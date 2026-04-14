#!/usr/bin/env python3
"""
lab_start.py — Next-gen lab readiness TUI for Arista Containerized Labs.

Invoked by VS Code tasks.json on folderOpen. Parses the clab topology,
watches every node in parallel for TCP:22 reachability, and renders a live,
role-grouped status table. On success, writes a LAB-READY.md dashboard that
the PacketAnglers/lab-dashboard extension auto-opens in a clickable webview.

Intentional design choices:
  * asyncio + raw TCP probes (no paramiko): fast, cheap, no credential handling.
    "Port 22 accepts a connection" is a better 'lab is up' signal than SSH auth
    (which can succeed before startup-config finishes applying).
  * Per-node timeout, not a shared budget. Slow nodes can't starve fast ones.
  * Optional .vscode/lab.yml provides canonical lab metadata (display name,
    credentials, validated-with versions, tips). See `LabConfig` for the
    full schema.
  * Stdlib + rich + pyyaml only. No extra deps to pull into the base image.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml
from rich.align import Align
from rich.console import Console, Group, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text
from rich.theme import Theme


# ─────────────────────────────────────────────────────────────────────────────
# Defaults
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_PER_NODE_TIMEOUT = 420      # 7 min — generous for cold cEOS + startup-config
DEFAULT_PROBE_PORT = 22
DEFAULT_PROBE_INTERVAL = 2.0        # seconds between probe attempts
DEFAULT_CONNECT_TIMEOUT = 2.0       # seconds per TCP connect attempt
DEFAULT_REFRESH_HZ = 8              # Rich Live refresh rate


THEME = Theme({
    "brand.c": "grey70",
    "brand.a": "red",
    "brand.r": "green",
    "brand.l": "bold cyan",
    "lab.name": "bold white on blue",
    "status.pending": "dim",
    "status.probing": "yellow",
    "status.ready": "bold green",
    "status.timeout": "bold red",
    "status.error": "bold red",
    "info": "bold cyan",
    "warning": "bold yellow",
    "critical": "bold red",
    "success": "bold green",
    "muted": "grey50",
})


# ─────────────────────────────────────────────────────────────────────────────
# Domain model
# ─────────────────────────────────────────────────────────────────────────────

class NodeStatus(str, Enum):
    PENDING = "pending"     # not yet probed
    PROBING = "probing"     # in-flight
    READY = "ready"         # TCP:22 accepted
    TIMEOUT = "timeout"     # exceeded per-node budget
    ERROR = "error"         # unexpected exception


@dataclass
class Node:
    name: str
    kind: str
    mgmt_ip: Optional[str]
    role: str
    status: NodeStatus = NodeStatus.PENDING
    started_at: Optional[float] = None
    ready_at: Optional[float] = None
    attempts: int = 0
    last_error: Optional[str] = None

    @property
    def elapsed(self) -> float:
        if self.started_at is None:
            return 0.0
        end = self.ready_at if self.ready_at else time.monotonic()
        return end - self.started_at


@dataclass
class LabConfig:
    # ── Core (always populated from topology) ─────────────────────────────
    name: str                              # from topology.clab.yml `name:`
    topology_path: Path
    nodes: list[Node]

    # ── Display (from lab.yml `display:`) ─────────────────────────────────
    display_name: Optional[str] = None     # human-friendly name
    subtitle: Optional[str] = None
    documentation_url: Optional[str] = None  # external link (e.g. tech-library guide)
    validated_with: dict = field(default_factory=dict)   # {cEOS: "4.35.2F", ...}
    resources: dict = field(default_factory=dict)        # {cpus: 16, memory: "64 GB", ...}

    # ── Credentials (from lab.yml `credentials:`) ─────────────────────────
    username: str = "admin"
    password: str = "admin"

    # ── Boot behavior (from lab.yml `boot:`) ──────────────────────────────
    per_node_timeout: int = DEFAULT_PER_NODE_TIMEOUT
    probe_port: int = DEFAULT_PROBE_PORT
    preflight_notes: list[str] = field(default_factory=list)
    skip_nodes: set[str] = field(default_factory=set)

    # ── Dashboard (from lab.yml `dashboard:`) ─────────────────────────────
    auto_open_dashboard: bool = True
    tips: list[str] = field(default_factory=list)

    @property
    def lab_root(self) -> Path:
        return self.topology_path.parent.parent

    @property
    def heading(self) -> str:
        """Prefer the human-friendly display name; fall back to clab topology name."""
        return self.display_name or self.name


# Role inference — purely heuristic, overridable via lab.yml
ROLE_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"SPINE", re.IGNORECASE), "Spine"),
    (re.compile(r"LEAF", re.IGNORECASE), "Leaf"),
    (re.compile(r"BORDER", re.IGNORECASE), "Border"),
    (re.compile(r"^(host|server|client|pc)", re.IGNORECASE), "Host"),
    (re.compile(r"^(cv|cvp)", re.IGNORECASE), "CVP"),
]

# Display order when grouping the status table
ROLE_ORDER = ["Spine", "Leaf", "Border", "Router", "Host", "CVP", "Linux", "Other"]


def infer_role(name: str, kind: str) -> str:
    for pattern, role in ROLE_RULES:
        if pattern.search(name):
            return role
    if kind == "arista_ceos":
        return "Router"
    if kind == "linux":
        return "Linux"
    return "Other"


# ─────────────────────────────────────────────────────────────────────────────
# Loading
# ─────────────────────────────────────────────────────────────────────────────

def find_topology_path() -> Path:
    """Locate topology.clab.yml — env var first, then lab-root fallback."""
    # env var set by the base container
    env_ws = os.getenv("CONTAINERWSF")
    candidates: list[Path] = []
    if env_ws:
        candidates.append(Path(env_ws) / "clab" / "topology.clab.yml")

    # fallback: walk up from script location looking for clab/topology.clab.yml
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        candidates.append(parent / "clab" / "topology.clab.yml")

    # also try cwd — tasks.json defaults cwd to ${workspaceFolder}
    candidates.append(Path.cwd() / "clab" / "topology.clab.yml")

    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError(
        "Could not locate clab/topology.clab.yml. Checked:\n  "
        + "\n  ".join(str(c) for c in candidates)
    )


def load_lab_overrides(lab_root: Path) -> dict:
    """Load optional .vscode/lab.yml if present."""
    override_path = lab_root / ".vscode" / "lab.yml"
    if not override_path.is_file():
        return {}
    try:
        with override_path.open() as f:
            return yaml.safe_load(f) or {}
    except Exception as exc:
        # Don't die on a broken override — just warn and continue with defaults
        print(f"[warn] failed to parse {override_path}: {exc}", file=sys.stderr)
        return {}


def load_lab_config() -> LabConfig:
    topology_path = find_topology_path()
    lab_root = topology_path.parent.parent

    with topology_path.open() as f:
        topo = yaml.safe_load(f)

    lab_name = topo.get("name", "unnamed-lab")
    nodes_dict = topo.get("topology", {}).get("nodes", {}) or {}

    overrides = load_lab_overrides(lab_root)

    # Nested sections — each one is optional; defaults kick in when absent.
    display   = overrides.get("display", {}) or {}
    creds     = overrides.get("credentials", {}) or {}
    boot      = overrides.get("boot", {}) or {}
    dashboard = overrides.get("dashboard", {}) or {}

    role_overrides = boot.get("roles", {}) or {}
    skip = set(boot.get("skip_nodes", []) or [])

    nodes: list[Node] = []
    for name, spec in nodes_dict.items():
        if name in skip:
            continue
        spec = spec or {}
        kind = spec.get("kind", "unknown")
        mgmt_ip = spec.get("mgmt-ipv4") or spec.get("mgmt-ipv6")
        role = role_overrides.get(name) or infer_role(name, kind)
        nodes.append(Node(name=name, kind=kind, mgmt_ip=mgmt_ip, role=role))

    return LabConfig(
        name=lab_name,
        topology_path=topology_path,
        nodes=nodes,
        # display
        display_name=display.get("name"),
        subtitle=display.get("subtitle"),
        documentation_url=display.get("documentation_url"),
        validated_with=dict(display.get("validated_with", {}) or {}),
        resources=dict(display.get("resources", {}) or {}),
        # credentials — env vars still win (useful for CI / one-off overrides)
        username=os.getenv("LABUSERNAME", creds.get("username", "admin")),
        password=os.getenv("LABPASSPHRASE", creds.get("password", "admin")),
        # boot
        per_node_timeout=int(boot.get("per_node_timeout", DEFAULT_PER_NODE_TIMEOUT)),
        probe_port=int(boot.get("probe_port", DEFAULT_PROBE_PORT)),
        preflight_notes=list(boot.get("preflight_notes", []) or []),
        skip_nodes=skip,
        # dashboard
        auto_open_dashboard=bool(dashboard.get("auto_open", True)),
        tips=list(dashboard.get("tips", []) or []),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Probing
# ─────────────────────────────────────────────────────────────────────────────

async def tcp_probe(host: str, port: int, timeout: float) -> Optional[str]:
    """Attempt a single TCP connect. Returns None on success, error string on failure."""
    try:
        fut = asyncio.open_connection(host=host, port=port)
        reader, writer = await asyncio.wait_for(fut, timeout=timeout)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return None
    except asyncio.TimeoutError:
        return "connect timeout"
    except (ConnectionRefusedError, OSError) as exc:
        return f"{type(exc).__name__}: {exc}"
    except Exception as exc:  # defensive — don't let a probe bug kill the watcher
        return f"{type(exc).__name__}: {exc}"


async def watch_node(node: Node, cfg: LabConfig) -> None:
    """Retry TCP probes until the node accepts a connection or per-node budget expires."""
    node.status = NodeStatus.PROBING
    node.started_at = time.monotonic()
    deadline = node.started_at + cfg.per_node_timeout

    # Prefer container-hostname resolution (clab wires up DNS); fall back to mgmt IP.
    targets: list[str] = [node.name]
    if node.mgmt_ip and node.mgmt_ip not in targets:
        targets.append(node.mgmt_ip)

    while True:
        node.attempts += 1
        for target in targets:
            err = await tcp_probe(target, cfg.probe_port, DEFAULT_CONNECT_TIMEOUT)
            if err is None:
                node.status = NodeStatus.READY
                node.ready_at = time.monotonic()
                return
            node.last_error = f"{target}: {err}"

        if time.monotonic() >= deadline:
            node.status = NodeStatus.TIMEOUT
            node.ready_at = time.monotonic()
            return

        await asyncio.sleep(DEFAULT_PROBE_INTERVAL)


# ─────────────────────────────────────────────────────────────────────────────
# Rendering
# ─────────────────────────────────────────────────────────────────────────────

def build_banner(cfg: LabConfig) -> RenderableType:
    """Hero banner: lab name front-and-center, cArL branding as subtitle."""
    brand = Text()
    brand.append("c", style="brand.c")
    brand.append("A", style="brand.a")
    brand.append("r", style="brand.r")
    brand.append("L", style="brand.l")
    brand.append("  ·  Containerized Arista Labs", style="muted")

    lab_label = Text()
    lab_label.append(" ", style="")
    lab_label.append(f" {cfg.heading} ", style="lab.name")
    lab_label.append("  ", style="")
    lab_label.append(f"{len(cfg.nodes)} nodes", style="info")

    body = Group(
        Align.center(brand),
        Text(""),
        Align.center(lab_label),
    )
    return Panel(body, border_style="cyan", padding=(1, 4), expand=True)


def build_preflight_panel(cfg: LabConfig) -> RenderableType:
    lines: list[RenderableType] = []

    creds = Text()
    creds.append("Credentials: ", style="info")
    creds.append(f"{cfg.username} / {cfg.password}", style="bold")
    lines.append(creds)

    readme = cfg.topology_path.parent.parent / "README.md"
    if readme.is_file():
        rline = Text()
        rline.append("Docs: ", style="info")
        rline.append(str(readme.relative_to(Path.cwd()) if readme.is_relative_to(Path.cwd()) else readme), style="bold")
        rline.append(" — skim before you lab", style="muted")
        lines.append(rline)

    for note in cfg.preflight_notes:
        lines.append(Text(f"• {note}", style="warning"))

    return Panel(
        Group(*lines),
        title="[info]Pre-flight[/info]",
        border_style="cyan",
        padding=(0, 2),
        expand=True,
    )


# Spinner pre-built once; Rich handles frame advancement per-render.
_PROBING_SPINNER = Spinner("dots", style="status.probing")
_STATUS_GLYPH = {
    NodeStatus.PENDING: Text("○", style="status.pending"),
    NodeStatus.READY:   Text("●", style="status.ready"),
    NodeStatus.TIMEOUT: Text("✗", style="status.timeout"),
    NodeStatus.ERROR:   Text("!", style="status.error"),
}


def _status_cell(node: Node) -> RenderableType:
    if node.status == NodeStatus.PROBING:
        return _PROBING_SPINNER
    return _STATUS_GLYPH[node.status]


def _status_label(node: Node) -> Text:
    label_map = {
        NodeStatus.PENDING: ("pending", "status.pending"),
        NodeStatus.PROBING: ("pending", "status.probing"),
        NodeStatus.READY:   ("ready",   "status.ready"),
        NodeStatus.TIMEOUT: ("timeout", "status.timeout"),
        NodeStatus.ERROR:   ("error",   "status.error"),
    }
    text, style = label_map[node.status]
    return Text(text, style=style)


def _fmt_elapsed(seconds: float) -> str:
    if seconds <= 0:
        return "—"
    if seconds < 60:
        return f"{seconds:4.1f}s"
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:d}m{secs:02d}s"


def build_status_table(cfg: LabConfig) -> RenderableType:
    """Live-updating table grouped by role."""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="grey35",
        expand=True,
        pad_edge=False,
    )
    table.add_column("", width=2, no_wrap=True)                  # status glyph
    table.add_column("Node", style="bold", no_wrap=True)
    table.add_column("Role", style="muted", no_wrap=True)
    table.add_column("Kind", style="muted", no_wrap=True)
    table.add_column("Mgmt IP", style="muted", no_wrap=True)
    table.add_column("Status", no_wrap=True)
    table.add_column("Elapsed", justify="right", style="muted", no_wrap=True)

    # Group by role, in ROLE_ORDER. Unknown roles go to the end alphabetically.
    by_role: dict[str, list[Node]] = {}
    for node in cfg.nodes:
        by_role.setdefault(node.role, []).append(node)

    ordered_roles: list[str] = [r for r in ROLE_ORDER if r in by_role]
    ordered_roles += sorted(r for r in by_role if r not in ROLE_ORDER)

    first = True
    for role in ordered_roles:
        if not first:
            table.add_section()
        first = False
        for node in sorted(by_role[role], key=lambda n: n.name):
            table.add_row(
                _status_cell(node),
                node.name,
                node.role,
                node.kind,
                node.mgmt_ip or "—",
                _status_label(node),
                _fmt_elapsed(node.elapsed),
            )
    return table


def build_footer(cfg: LabConfig, started_at: float) -> RenderableType:
    ready = sum(1 for n in cfg.nodes if n.status == NodeStatus.READY)
    timeout = sum(1 for n in cfg.nodes if n.status == NodeStatus.TIMEOUT)
    total = len(cfg.nodes)
    elapsed = time.monotonic() - started_at

    t = Text()
    t.append("  Ready ", style="muted")
    t.append(f"{ready}/{total}", style="status.ready" if ready == total else "info")
    if timeout:
        t.append("   Timeout ", style="muted")
        t.append(str(timeout), style="status.timeout")
    t.append("   Elapsed ", style="muted")
    t.append(_fmt_elapsed(elapsed), style="bold")
    return t


def build_live_layout(cfg: LabConfig, started_at: float) -> RenderableType:
    return Group(
        build_banner(cfg),
        build_preflight_panel(cfg),
        build_status_table(cfg),
        build_footer(cfg, started_at),
    )


def _build_command_uri(command_id: str, *args: object) -> str:
    """
    Build a `command:<id>?<url-encoded-json-array>` URI.
    Args are url-encoded as a JSON array → spread positionally on dispatch.
    """
    if args:
        encoded = urllib.parse.quote(json.dumps(list(args)), safe="")
        return f"command:{command_id}?{encoded}"
    return f"command:{command_id}"


def _build_topology_view_uri(cfg: LabConfig) -> str:
    """
    Use the lab-dashboard extension's openTopology command, which awaits
    vscode.open before firing topoViewer — sidesteps the active-editor race
    that breaks the naive runCommands chain.
    """
    return _build_command_uri("labDashboard.openTopology", str(cfg.topology_path))


def _build_open_file_uri(path: Path) -> str:
    """Use the lab-dashboard extension's openFile (handles Uri.file conversion)."""
    return _build_command_uri("labDashboard.openFile", str(path))


# ─────────────────────────────────────────────────────────────────────────────
# Dashboard (auto-opened LAB-READY.md)
# ─────────────────────────────────────────────────────────────────────────────

DASHBOARD_FILENAME = "LAB-READY.md"


def build_dashboard_markdown(cfg: LabConfig, total_elapsed: float) -> str:
    """
    Generate the auto-open lab dashboard — a markdown surface the
    lab-dashboard extension renders with clickable command: URIs.
    """
    readme_path = cfg.lab_root / "README.md"
    lines: list[str] = []

    # ── Header ──
    # Lab heading prefers display.name (human-friendly) over clab topology name.
    lines.append(f"# 🧪 {cfg.heading}")
    lines.append("")
    if cfg.subtitle:
        lines.append(f"_{cfg.subtitle}_")
        lines.append("")

    # Status line — compact, no credentials (they get their own block).
    lines.append(
        f"🟢 **Lab Ready** &nbsp;·&nbsp; "
        f"{len(cfg.nodes)} nodes up in {_fmt_elapsed(total_elapsed)}"
    )
    lines.append("")

    # Credentials — own block, prominent. Wrapper class lets the extension's
    # CSS style the <code> values as chip/pill badges instead of inline code.
    lines.append('<div class="lab-credentials">')
    lines.append(
        f'<span class="lab-credentials-label">Credentials</span>'
        f'<code class="lab-cred">{cfg.username}</code>'
        f'<span class="lab-cred-sep">/</span>'
        f'<code class="lab-cred">{cfg.password}</code>'
    )
    lines.append("</div>")
    lines.append("")

    # Validated-with badge row — each entry becomes a styled pill.
    if cfg.validated_with:
        lines.append('<div class="lab-validated-with">')
        lines.append('<span class="lab-validated-label">Validated with</span>')
        for k, v in cfg.validated_with.items():
            lines.append(
                f'<span class="lab-badge">'
                f'<span class="lab-badge-key">{k}</span>'
                f'<span class="lab-badge-val">{v}</span>'
                f'</span>'
            )
        lines.append("</div>")
        lines.append("")

    # Resources row — same badge styling, different label.
    if cfg.resources:
        lines.append('<div class="lab-validated-with">')
        lines.append('<span class="lab-validated-label">Resources</span>')
        for k, v in cfg.resources.items():
            lines.append(
                f'<span class="lab-badge">'
                f'<span class="lab-badge-key">{k}</span>'
                f'<span class="lab-badge-val">{v}</span>'
                f'</span>'
            )
        lines.append("</div>")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ── Quick Actions ──
    lines.append("## 🚀 Quick Actions")
    lines.append("")

    if cfg.documentation_url:
        lines.append(f"### [📖 &nbsp; Tech Library Guide]({cfg.documentation_url})")
        lines.append("")
        lines.append(f"External deployment guide on [tech-library.arista.com](https://tech-library.arista.com). Opens in your browser.")
        lines.append("")

    lines.append(f"### [🔭 &nbsp; Open Topology View]({_build_topology_view_uri(cfg)})")
    lines.append("")
    lines.append("Launch the interactive ContainerLab topology graph in a new editor tab.")
    lines.append("")

    if readme_path.is_file():
        lines.append(f"### [📚 &nbsp; Open README]({_build_open_file_uri(readme_path)})")
        lines.append("")
        lines.append("Lab documentation, walkthrough, and operational instructions (build / deploy / validate).")
        lines.append("")

    lines.append(f"### [📂 &nbsp; Open Topology File]({_build_open_file_uri(cfg.topology_path)})")
    lines.append("")
    lines.append("Inspect or edit the `topology.clab.yml` source.")
    lines.append("")

    # ── Node inventory ──
    lines.append("---")
    lines.append("")
    lines.append("## 🔌 Node Inventory")
    lines.append("")
    lines.append("| Role | Node | Kind | Mgmt IP |")
    lines.append("|------|------|------|---------|")

    def role_sort_key(n: Node) -> tuple[int, str]:
        idx = ROLE_ORDER.index(n.role) if n.role in ROLE_ORDER else 99
        return (idx, n.name)

    for n in sorted(cfg.nodes, key=role_sort_key):
        lines.append(f"| {n.role} | `{n.name}` | {n.kind} | `{n.mgmt_ip or '—'}` |")
    lines.append("")

    # ── Tips ──
    if cfg.tips:
        lines.append("---")
        lines.append("")
        lines.append("## 💡 Tips")
        lines.append("")
        for tip in cfg.tips:
            lines.append(f"- {tip}")
        lines.append("")

    # ── Footer ──
    lines.append("---")
    lines.append("")
    lines.append(
        "<sub>Auto-generated by <code>lab_start.py</code> on lab readiness. "
        "Close this tab with <kbd>Ctrl</kbd>+<kbd>W</kbd>.</sub>"
    )
    lines.append("")

    return "\n".join(lines)


def write_and_open_dashboard(cfg: LabConfig, total_elapsed: float, console: Console) -> Optional[Path]:
    """
    Write the dashboard to <lab_root>/LAB-READY.md.

    The Arista Labs Dashboard extension (packetanglers.aristalabs-dashboard)
    watches for this file and auto-opens it in its custom webview, which
    renders the markdown with clickable command: URIs.

    Returns the dashboard path on success, None on write failure.
    """
    dashboard_path = cfg.lab_root / DASHBOARD_FILENAME
    try:
        dashboard_path.write_text(build_dashboard_markdown(cfg, total_elapsed))
    except Exception as exc:
        console.print(f"[warning]Failed to write dashboard:[/warning] {exc}")
        return None
    return dashboard_path


def build_ready_panel(cfg: LabConfig, total_elapsed: float, dashboard_path: Optional[Path] = None) -> RenderableType:
    body: list[RenderableType] = []

    summary = Text()
    summary.append("🧪🥼  ", style="")
    summary.append("The lab is ready! Happy Labbing!", style="success")
    summary.append(f"   {len(cfg.nodes)} nodes up in {_fmt_elapsed(total_elapsed)}", style="muted")
    body.append(summary)
    body.append(Text(""))

    creds = Text()
    creds.append("SSH: ", style="info")
    creds.append(f"ssh {cfg.username}@<node>", style="bold")
    creds.append(f"   (password: {cfg.password})", style="muted")
    body.append(creds)

    if dashboard_path is not None:
        body.append(Text(""))
        dash = Text()
        dash.append("📋 Dashboard: ", style="info")
        dash.append(str(dashboard_path.name), style="bold")
        dash.append(" opened — click the buttons to go.", style="muted")
        body.append(dash)

    return Panel(
        Group(*body),
        title="[success]Lab Ready[/success]",
        border_style="green",
        padding=(1, 2),
        expand=True,
    )


def build_failure_panel(cfg: LabConfig, total_elapsed: float) -> RenderableType:
    failed = [n for n in cfg.nodes if n.status != NodeStatus.READY]
    body: list[RenderableType] = []

    summary = Text()
    summary.append("⚠  ", style="")
    summary.append(f"{len(failed)} of {len(cfg.nodes)} nodes did not come up", style="critical")
    summary.append(f"   (after {_fmt_elapsed(total_elapsed)})", style="muted")
    body.append(summary)
    body.append(Text(""))

    body.append(Text("Failing nodes:", style="warning"))
    for n in failed:
        line = Text()
        line.append(f"  • {n.name}", style="bold")
        line.append(f" ({n.role}, {n.kind})", style="muted")
        if n.last_error:
            line.append(f" — last error: {n.last_error}", style="muted")
        body.append(line)

    body.append(Text(""))
    body.append(Text("Remediation:", style="info"))
    body.append(Text("  → sudo containerlab inspect --topo clab/topology.clab.yml", style=""))
    for n in failed[:3]:  # cap the per-node suggestions to keep the panel tight
        body.append(Text(f"  → docker logs clab-{cfg.name}-{n.name}", style=""))
    if len(failed) > 3:
        body.append(Text(f"  → …and similar for the other {len(failed) - 3} failing node(s)", style="muted"))
    body.append(Text("  → make stop && make start    # nuke and pave", style=""))

    return Panel(
        Group(*body),
        title="[critical]Lab Incomplete[/critical]",
        border_style="red",
        padding=(1, 2),
        expand=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Orchestration
# ─────────────────────────────────────────────────────────────────────────────

async def run(cfg: LabConfig, console: Console) -> int:
    started_at = time.monotonic()

    # Nuke any stale LAB-READY.md from a prior session. The dashboard's
    # existence is the "lab ready" signal the extension watches for; we don't
    # want it auto-opening with stale data while we're still booting.
    stale_dashboard = cfg.lab_root / DASHBOARD_FILENAME
    if stale_dashboard.is_file():
        try:
            stale_dashboard.unlink()
        except Exception as exc:
            console.print(f"[muted]Could not remove stale {DASHBOARD_FILENAME}: {exc}[/muted]")

    # Launch one watcher per node.
    tasks = [asyncio.create_task(watch_node(n, cfg), name=f"watch:{n.name}") for n in cfg.nodes]

    with Live(
        build_live_layout(cfg, started_at),
        console=console,
        refresh_per_second=DEFAULT_REFRESH_HZ,
        transient=False,
    ) as live:
        # Poll-based update loop — lets us drive the spinner + elapsed timers.
        while not all(t.done() for t in tasks):
            live.update(build_live_layout(cfg, started_at))
            await asyncio.sleep(1 / DEFAULT_REFRESH_HZ)
        # Final render of live layout before we move on.
        live.update(build_live_layout(cfg, started_at))

    # Surface any unexpected exceptions from watcher tasks.
    for t in tasks:
        if t.cancelled():
            continue
        exc = t.exception()
        if exc is not None:
            # Map back to the node if we can.
            name = t.get_name().removeprefix("watch:")
            for n in cfg.nodes:
                if n.name == name:
                    n.status = NodeStatus.ERROR
                    n.last_error = f"{type(exc).__name__}: {exc}"
                    break

    total_elapsed = time.monotonic() - started_at
    all_ready = all(n.status == NodeStatus.READY for n in cfg.nodes)

    console.print()
    if all_ready:
        dashboard_path = None
        if cfg.auto_open_dashboard:
            dashboard_path = write_and_open_dashboard(cfg, total_elapsed, console)
        console.print(build_ready_panel(cfg, total_elapsed, dashboard_path=dashboard_path))
        return 0
    console.print(build_failure_panel(cfg, total_elapsed))
    return 1


def main() -> int:
    console = Console(theme=THEME, log_path=False)
    try:
        cfg = load_lab_config()
    except Exception as exc:
        console.print(f"[critical]Failed to load lab config:[/critical] {exc}")
        return 2

    if not cfg.nodes:
        console.print("[warning]No nodes defined in topology. Nothing to wait on.[/warning]")
        return 0

    try:
        return asyncio.run(run(cfg, console))
    except KeyboardInterrupt:
        console.print("\n[warning]Interrupted.[/warning]")
        return 130


if __name__ == "__main__":
    sys.exit(main())
