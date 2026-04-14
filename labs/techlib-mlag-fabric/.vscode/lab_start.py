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

Author: Mitch & Claude, morning coffee edition ☕
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
DEFAULT_SSH_TIMEOUT = 5.0           # seconds for an SSH handshake+auth probe; slightly
                                    # generous because cold cEOS takes longer for sshd
                                    # to respond once it first accepts a connection
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
    PENDING = "pending"                        # not yet probed
    PROBING_TCP = "probing_tcp"                # waiting for port 22 to accept connections
    PROBING_SSH = "probing_ssh"                # port open; waiting for SSH handshake + auth offer
    READY = "ready"                            # SSH reaches auth stage via hostname — node truly ready
    FAILED_HOSTNAME = "failed_hostname"        # reachable by IP, but hostname doesn't resolve
    TIMEOUT = "timeout"                        # exceeded per-node budget
    ERROR = "error"                            # unexpected exception


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


async def ssh_probe(host: str, username: str, timeout: float) -> Optional[str]:
    """
    Run a one-shot non-interactive SSH probe to verify the server has progressed
    past early init into a state where it can actually accept authentication.

    TCP-accept on port 22 happens as soon as sshd is listening, which can be
    well before userspace (PAM, AAA, /etc/hosts, VRF config) is ready to
    actually authenticate anyone. So after TCP succeeds, we run a real SSH
    invocation with BatchMode to detect the auth-offered phase.

    Returns None (success) when the server has progressed far enough to have
    offered authentication methods and rejected our probe — which is the
    correct "node is ready" signal. The probe itself will always fail auth
    (no credentials supplied) but the failure mode tells us everything:

      * "Permission denied" stderr → server is alive, protocol exchange
        completed, auth methods were offered. READY.
      * "Connection refused" / "Could not resolve" / "Connection timed out"
        → server isn't reachable yet. Not ready.

    We specifically cannot rely on the ssh exit code alone — "Permission
    denied" exits 255 (same as transport failures), so we parse stderr to
    distinguish the two cases.

    Returns None on ready, or a short error string on failure. The error
    string surfaces the last meaningful stderr line so operators can see
    *why* a node is stuck (e.g., "Could not resolve hostname B-LEAF1" is
    a dead giveaway that /etc/hosts wasn't populated).
    """
    # Hard-code a per-call timeout slightly below the outer asyncio timeout so
    # ssh bails before asyncio rips the subprocess away — gives us the exit
    # code and stderr rather than a kill-9.
    ssh_connect_timeout = max(1, int(timeout) - 1)

    cmd = [
        "ssh",
        "-o", "BatchMode=yes",                       # never prompt; fail fast on password-required
        "-o", "StrictHostKeyChecking=no",            # first-boot host keys are new every time
        "-o", "UserKnownHostsFile=/dev/null",        # don't pollute ~/.ssh/known_hosts
        "-o", "LogLevel=ERROR",                      # suppress the "Warning: Permanently added" noise
        "-o", f"ConnectTimeout={ssh_connect_timeout}",
        f"{username}@{host}",
        "true",                                      # command to run if we ever got in — we won't
    ]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            try:
                await proc.wait()
            except Exception:
                pass
            return "ssh probe timeout"

        stderr_text = (stderr or b"").decode("utf-8", errors="replace")

        # Success case 1: exit 0 means the probe somehow got in and ran `true`.
        # Extraordinarily unlikely with BatchMode + no key, but treat as ready.
        if proc.returncode == 0:
            return None

        # Success case 2: the server reached the "offering auth methods" stage
        # and rejected our attempt. This is what we actually want to detect —
        # it proves sshd/PAM/AAA/hostname-resolution all made it through init.
        #
        # The exact stderr text varies slightly by OpenSSH version but always
        # contains "Permission denied" when auth was offered and rejected.
        # cEOS typically returns: "Permission denied (publickey,keyboard-interactive)."
        if "Permission denied" in stderr_text:
            return None

        # Failure cases. Surface the most useful line of stderr so the TUI's
        # diagnostic can show the operator exactly why.
        meaningful = [ln.strip() for ln in stderr_text.splitlines() if ln.strip()]
        if meaningful:
            return meaningful[-1]
        return f"ssh exit {proc.returncode}"
    except FileNotFoundError:
        # ssh binary not on PATH — shouldn't happen in the lab-base container,
        # but we want a clear error if it ever does rather than a cryptic traceback.
        return "ssh client not found on PATH"
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


async def watch_node(node: Node, cfg: LabConfig) -> None:
    """
    Two-phase readiness watcher.

    Phase 1 (PROBING_TCP): cheap TCP-accept probe on port 22 every interval.
    Phase 2 (PROBING_SSH): once TCP is open, spawn real ssh invocations to
    verify the server has progressed past early init to where it can actually
    serve the user's connection attempt.

    Both phases share the single per-node timeout budget. If the whole thing
    takes longer than cfg.per_node_timeout, the node is marked TIMEOUT.

    We probe by hostname (how the user will connect) and fall back to mgmt IP
    — this matches the user's likely invocation pattern and catches DNS /
    /etc/hosts population issues that would otherwise leave a node looking
    "ready" when it's actually unreachable by name.
    """
    node.status = NodeStatus.PROBING_TCP
    node.started_at = time.monotonic()
    deadline = node.started_at + cfg.per_node_timeout

    # Prefer container-hostname resolution (clab normally wires up /etc/hosts);
    # fall back to mgmt IP. The hostname is tried first because that's what
    # the user will use — if it doesn't resolve, we want to find out NOW, not
    # when the user copies a hostname from the dashboard and gets "no route".
    targets: list[str] = [node.name]
    if node.mgmt_ip and node.mgmt_ip not in targets:
        targets.append(node.mgmt_ip)

    # ── Phase 1: TCP accept ────────────────────────────────────────────────
    tcp_ready_target: Optional[str] = None
    while tcp_ready_target is None:
        node.attempts += 1
        for target in targets:
            err = await tcp_probe(target, cfg.probe_port, DEFAULT_CONNECT_TIMEOUT)
            if err is None:
                tcp_ready_target = target
                break
            node.last_error = f"{target}: {err}"

        if tcp_ready_target is not None:
            break

        if time.monotonic() >= deadline:
            node.status = NodeStatus.TIMEOUT
            node.ready_at = time.monotonic()
            return

        await asyncio.sleep(DEFAULT_PROBE_INTERVAL)

    # ── Phase 2: SSH handshake ─────────────────────────────────────────────
    #
    # "Ready" in the user-facing sense means "the user can `ssh admin@<name>`
    # and get a prompt". TCP being open is necessary but not sufficient. We
    # probe the hostname first (what the user will type) and fall back to the
    # mgmt IP. The failure modes are meaningfully different:
    #
    #   * Hostname fails with "Could not resolve" but IP succeeds → FAILED_HOSTNAME.
    #     The node is alive and reachable, but /etc/hosts is missing the entry
    #     (or has it case-mismatched). User must fix /etc/hosts to SSH by name.
    #
    #   * Hostname fails for a non-resolution reason (Connection refused,
    #     timeout, etc.) and IP also fails → keep retrying until TIMEOUT.
    #     The node is genuinely not ready yet.
    #
    #   * Hostname succeeds → READY, full stop. We don't need to also probe IP.
    node.status = NodeStatus.PROBING_SSH
    node.last_error = None  # clear TCP-phase errors; we're past that

    hostname_target = node.name
    ip_target = node.mgmt_ip if node.mgmt_ip and node.mgmt_ip != hostname_target else None

    while True:
        node.attempts += 1

        # Try hostname first — that's the "fully ready" path.
        hostname_err = await ssh_probe(hostname_target, cfg.username, DEFAULT_SSH_TIMEOUT)
        if hostname_err is None:
            node.status = NodeStatus.READY
            node.ready_at = time.monotonic()
            return

        # Hostname failed. What kind of failure?
        hostname_unresolvable = "Could not resolve" in hostname_err

        # If we have an IP fallback, test that. Being reachable by IP but not
        # by name is the exact signature of an /etc/hosts issue — we flag it
        # distinctly so the user knows to fix DNS, not wait longer.
        if ip_target:
            ip_err = await ssh_probe(ip_target, cfg.username, DEFAULT_SSH_TIMEOUT)
            if ip_err is None and hostname_unresolvable:
                node.status = NodeStatus.FAILED_HOSTNAME
                node.ready_at = time.monotonic()
                node.last_error = (
                    f"{hostname_target} does not resolve, but {ip_target} is reachable. "
                    f"Check /etc/hosts for an entry mapping {hostname_target} → {ip_target}."
                )
                return
            # Record whichever error is more diagnostic. If hostname was
            # unresolvable but IP is also unreachable, the node genuinely
            # isn't up yet — keep the IP error which is the actionable one.
            node.last_error = f"{ip_target}: {ip_err}" if ip_err else node.last_error
        else:
            node.last_error = f"{hostname_target}: {hostname_err}"

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
    NodeStatus.PENDING:          Text("○", style="status.pending"),
    NodeStatus.READY:            Text("●", style="status.ready"),
    NodeStatus.FAILED_HOSTNAME:  Text("⚠", style="status.timeout"),
    NodeStatus.TIMEOUT:          Text("✗", style="status.timeout"),
    NodeStatus.ERROR:            Text("!", style="status.error"),
}


def _status_cell(node: Node) -> RenderableType:
    if node.status in (NodeStatus.PROBING_TCP, NodeStatus.PROBING_SSH):
        return _PROBING_SPINNER
    return _STATUS_GLYPH[node.status]


def _status_label(node: Node) -> Text:
    # Phase-aware labels: operators should be able to tell at a glance whether
    # a slow node is stuck at "can't even open a socket" vs "TCP is fine but
    # sshd isn't letting me in yet" — different root causes, different fixes.
    label_map = {
        NodeStatus.PENDING:         ("pending",          "status.pending"),
        NodeStatus.PROBING_TCP:     ("PROBING TCP 22",   "status.probing"),
        NodeStatus.PROBING_SSH:     ("CHECK SSH PROMPT", "status.probing"),
        NodeStatus.READY:           ("ready",            "status.ready"),
        NodeStatus.FAILED_HOSTNAME: ("hostname?",        "status.timeout"),
        NodeStatus.TIMEOUT:         ("timeout",          "status.timeout"),
        NodeStatus.ERROR:           ("error",            "status.error"),
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
    hostname_fail = sum(1 for n in cfg.nodes if n.status == NodeStatus.FAILED_HOSTNAME)
    timeout = sum(1 for n in cfg.nodes if n.status == NodeStatus.TIMEOUT)
    total = len(cfg.nodes)
    elapsed = time.monotonic() - started_at

    t = Text()
    t.append("  Ready ", style="muted")
    t.append(f"{ready}/{total}", style="status.ready" if ready == total else "info")
    if hostname_fail:
        t.append("   Hostname ", style="muted")
        t.append(str(hostname_fail), style="status.timeout")
    if timeout:
        t.append("   Timeout ", style="muted")
        t.append(str(timeout), style="status.timeout")
    t.append("   Elapsed ", style="muted")
    t.append(_fmt_elapsed(elapsed), style="bold")

    # If nodes have been stuck in SSH phase for a noticeable while, surface the
    # most common error so the operator can see *why* without digging into the
    # failure panel (which only renders after timeout). This is the "why isn't
    # it working" question answered in-flight rather than post-mortem.
    stuck_ssh = [
        n for n in cfg.nodes
        if n.status == NodeStatus.PROBING_SSH and n.last_error and n.elapsed > 20
    ]
    if stuck_ssh and ready < total:
        # Normalize per-node specifics so errors of the same CLASS cluster
        # together when tallying. Hostnames and IPs vary per node but the
        # underlying failure is often identical across the fleet (e.g.,
        # "Could not resolve hostname" affecting every node), and we want
        # that to show as "22 nodes stuck", not "1 node stuck" × 22 times.
        def error_class(node: Node) -> str:
            raw = node.last_error or ""
            # Strip the "<target>: " prefix we add when storing
            msg = raw.split(": ", 1)[-1] if ": " in raw else raw
            # Mask the node's own name/IP from the message so similar errors
            # collapse. The node's hostname and mgmt_ip are likely mentioned.
            for needle in (node.name, node.mgmt_ip or ""):
                if needle:
                    msg = msg.replace(needle, "<host>")
            return msg

        error_counts: dict[str, int] = {}
        for n in stuck_ssh:
            ec = error_class(n)
            error_counts[ec] = error_counts.get(ec, 0) + 1
        top_err, top_count = max(error_counts.items(), key=lambda kv: kv[1])
        # Truncate aggressively — footer should stay one line.
        if len(top_err) > 90:
            top_err = top_err[:87] + "…"
        diag = Text()
        diag.append("\n  ⚠ ", style="warning")
        diag.append(f"{top_count} node(s) stuck at SSH: ", style="muted")
        diag.append(top_err, style="status.timeout")
        t.append_text(diag)

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
    not_ready = [n for n in cfg.nodes if n.status != NodeStatus.READY]
    hostname_issues = [n for n in not_ready if n.status == NodeStatus.FAILED_HOSTNAME]
    other_failures = [n for n in not_ready if n.status != NodeStatus.FAILED_HOSTNAME]

    body: list[RenderableType] = []

    summary = Text()
    summary.append("⚠  ", style="")
    summary.append(f"{len(not_ready)} of {len(cfg.nodes)} nodes not fully ready", style="critical")
    summary.append(f"   (after {_fmt_elapsed(total_elapsed)})", style="muted")
    body.append(summary)
    body.append(Text(""))

    # Hostname-resolution issues are *different* from genuine failures. The
    # nodes are alive and reachable by IP, so the lab may still be usable —
    # the user just can't SSH by hostname until /etc/hosts is fixed.
    if hostname_issues:
        body.append(Text("Hostname resolution issue — reachable by IP, not by name:", style="warning"))
        for n in hostname_issues:
            line = Text()
            line.append(f"  • {n.name}", style="bold")
            line.append(f" → ", style="muted")
            line.append(f"{n.mgmt_ip}", style="info")
            line.append(f" ({n.role}, {n.kind})", style="muted")
            body.append(line)
        body.append(Text(""))
        body.append(Text("  Fix: add entries to /etc/hosts so hostnames resolve to mgmt IPs.", style="muted"))
        body.append(Text(f"       You can still SSH to these nodes by IP in the meantime.", style="muted"))
        body.append(Text(""))

    if other_failures:
        body.append(Text("Unreachable nodes:", style="warning"))
        for n in other_failures:
            line = Text()
            line.append(f"  • {n.name}", style="bold")
            line.append(f" ({n.role}, {n.kind})", style="muted")
            if n.last_error:
                line.append(f" — last error: {n.last_error}", style="muted")
            body.append(line)

        body.append(Text(""))
        body.append(Text("Remediation:", style="info"))
        body.append(Text("  → sudo containerlab inspect --topo clab/topology.clab.yml", style=""))
        for n in other_failures[:3]:  # cap the per-node suggestions to keep the panel tight
            body.append(Text(f"  → docker logs clab-{cfg.name}-{n.name}", style=""))
        if len(other_failures) > 3:
            body.append(Text(f"  → …and similar for the other {len(other_failures) - 3} failing node(s)", style="muted"))
        body.append(Text("  → make stop && make start    # nuke and pave", style=""))

    # Choose panel tone: if ONLY hostname issues, it's a warning (not a critical
    # failure); if any node is genuinely unreachable, it's a hard failure.
    if other_failures:
        title = "[critical]Lab Incomplete[/critical]"
        border = "red"
    else:
        title = "[warning]Lab Ready with Warnings[/warning]"
        border = "yellow"

    return Panel(
        Group(*body),
        title=title,
        border_style=border,
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

    # Categorize node outcomes. FAILED_HOSTNAME is a "soft failure" — the node
    # is reachable by IP, so the lab is usable; we still open the dashboard
    # and return success, but also surface the hostname warning so the user
    # knows what to fix.
    all_ready = all(n.status == NodeStatus.READY for n in cfg.nodes)
    all_usable = all(
        n.status in (NodeStatus.READY, NodeStatus.FAILED_HOSTNAME)
        for n in cfg.nodes
    )

    console.print()
    if all_ready:
        dashboard_path = None
        if cfg.auto_open_dashboard:
            dashboard_path = write_and_open_dashboard(cfg, total_elapsed, console)
        console.print(build_ready_panel(cfg, total_elapsed, dashboard_path=dashboard_path))
        return 0
    if all_usable:
        # Partial success: all nodes are reachable by IP, but some have
        # hostname resolution issues. Open the dashboard (lab works) AND
        # print the failure panel (so the user sees what to fix).
        dashboard_path = None
        if cfg.auto_open_dashboard:
            dashboard_path = write_and_open_dashboard(cfg, total_elapsed, console)
        console.print(build_failure_panel(cfg, total_elapsed))
        if dashboard_path:
            console.print()
            console.print(f"[info]Dashboard opened:[/info] {dashboard_path}")
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
