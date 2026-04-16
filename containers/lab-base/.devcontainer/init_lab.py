#!/usr/bin/env python3
"""
init_lab.py — Lab readiness TUI for Arista Containerized Labs (cArL).

Lives at /bin/init_lab.py in the lab-base container — a shared utility
that operates on whatever lab directory it's invoked from. Invoked by
VS Code tasks.json on folderOpen, or manually from the shell:

    init_lab.py                 # use current working directory
    init_lab.py --lab-dir PATH  # explicit lab directory

Discovery: a lab directory must contain BOTH:
  * clab/topology.clab.yml   — the containerlab topology
  * .vscode/lab.yml          — the dashboard/init metadata

Behavior:
  1. Pre-flight: write per-node Host aliases to ~/.ssh/config so the user
     can `ssh admin@<node>` in either case (canonical or lowercase). We
     can't reliably populate /etc/hosts in a Docker container — it's
     bind-mounted from the runtime layer — but ~/.ssh/config is a normal
     file that ssh honors at the application layer.
  2. For each node, run a two-phase probe:
       PROBING_TCP  — wait for port 22 to accept connections
       PROBING_SSH  — actually log in and run a no-op command to verify
                      auth works (kind-aware: cEOS gets `!`, Linux gets
                      `true`; both authenticated via sshpass).
  3. On success: render a LAB-READY.md dashboard that the PacketAnglers
     lab-dashboard extension auto-opens in a webview.

Design choices:
  * asyncio + sshpass/ssh subprocesses: no paramiko, kind-aware login
    test — the strongest possible "ready" signal.
  * Per-node timeout, not a shared budget — slow nodes can't starve fast ones.
  * ~/.ssh/config for user-facing hostname ergonomics; probes use IP for
    reliability. Two layers, neither fighting Docker's /etc/hosts.
  * Stdlib + rich + pyyaml + system ssh/sshpass — all present in lab-base.

Author: Mitch & Claude
"""

from __future__ import annotations

import argparse
import asyncio
import html
import json
import os
import re
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

# Footer-diagnostic tunables. The diagnostic is the "why is my node stuck?"
# message we surface in real-time during boot to save the operator from
# having to wait for the failure panel.
STUCK_SSH_AGE_SEC = 20              # node must be in PROBING_SSH this long
                                    # before its error is considered worth surfacing
DIAG_MSG_MAX_LEN = 90               # absolute max chars in the surfaced diagnostic;
                                    # footer is meant to stay one line
DIAG_MSG_TRUNCATE_AT = DIAG_MSG_MAX_LEN - 3  # leave room for the trailing ellipsis


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
    READY = "ready"                            # SSH login succeeded — node truly ready for the user
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

def resolve_lab_dir(explicit: Optional[Path] = None) -> Path:
    """
    Determine which lab directory to operate on.

    `init_lab.py` lives at /bin/init_lab.py in the lab-base container — it's a
    shared utility, not a per-lab artifact. So unlike older versions, the
    script's own location tells us nothing about which lab is being booted.
    Discovery is now explicit:

      1. If --lab-dir was passed on the command line, use that.
      2. Otherwise, use the current working directory.

    A lab directory is identified by the presence of BOTH:
      * clab/topology.clab.yml  — the containerlab topology
      * .vscode/lab.yml         — the dashboard/init metadata

    If those files aren't present at the resolved location, we fail loud
    with an explicit message naming what's expected and where we looked,
    so the user knows whether they're in the wrong directory or whether
    something's actually missing.
    """
    lab_dir = (explicit if explicit else Path.cwd()).resolve()
    topology = lab_dir / "clab" / "topology.clab.yml"
    lab_yml = lab_dir / ".vscode" / "lab.yml"

    if topology.is_file() and lab_yml.is_file():
        return lab_dir

    # Build a clear, actionable error. Distinguish "wrong dir entirely" from
    # "right dir, missing one file" so the user knows what to fix.
    missing = []
    if not topology.is_file():
        missing.append(f"clab/topology.clab.yml (expected at {topology})")
    if not lab_yml.is_file():
        missing.append(f".vscode/lab.yml (expected at {lab_yml})")

    source = (
        "(from --lab-dir)" if explicit
        else f"(from current working directory: {Path.cwd()})"
    )
    raise FileNotFoundError(
        f"Not a valid lab directory: {lab_dir} {source}\n"
        f"Missing:\n  - " + "\n  - ".join(missing) + "\n\n"
        f"Tip: cd into a lab directory and re-run, or use:\n"
        f"  init_lab.py --lab-dir /path/to/lab"
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
        # Don't die on a broken override — just warn and continue with defaults.
        # Plain print here (not console.print) because this runs during config
        # load, before the Rich Console is constructed in main().
        print(f"[warn] failed to parse {override_path}: {exc}", file=sys.stderr)
        return {}


def load_lab_config(lab_dir: Optional[Path] = None) -> LabConfig:
    lab_root = resolve_lab_dir(lab_dir)
    topology_path = lab_root / "clab" / "topology.clab.yml"

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
# SSH config pre-flight
# ─────────────────────────────────────────────────────────────────────────────

# Sentinel comments delimit the block we manage. Any content outside the
# markers is preserved verbatim — we never touch user-authored ssh config.
SSH_CONFIG_BEGIN_MARK = "# >>> aclabs init_lab.py — managed block (do not edit) >>>"
SSH_CONFIG_END_MARK   = "# <<< aclabs init_lab.py — managed block <<<"


def populate_ssh_config(cfg: LabConfig, console: Console) -> None:
    """
    Write per-node Host entries to ~/.ssh/config so the user can SSH to nodes
    by hostname (in any case) regardless of /etc/hosts state.

    Why not /etc/hosts? In Docker containers, /etc/hosts is bind-mounted from
    the runtime layer and managed by Docker itself — our writes get silently
    reverted. ssh config is a normal file in the user's home directory that
    Docker doesn't touch.

    The tradeoff: only `ssh` honors this file. `ping`, `curl`, etc. still go
    through /etc/hosts. For a lab environment where ssh is the dominant use
    case, that's an acceptable scope.

    For each node we write a stanza like:

        Host A-SPINE1 a-spine1
            HostName 172.100.100.10
            User admin

    Both canonical and lowercase forms appear as `Host` aliases, so
    `ssh A-SPINE1` and `ssh a-spine1` both find the entry and ssh substitutes
    the IP at connect time. Doesn't depend on hostname resolution at all.

    Idempotent: a managed block (delimited by sentinel comments) is rewritten
    each call. Anything outside the markers is preserved.

    Best-effort: failures are logged to the console and swallowed. Probes can
    still proceed by IP if this fails, so a non-writable ~/.ssh just means
    degraded user-facing ergonomics, not a broken boot.
    """
    ssh_config_path = Path.home() / ".ssh" / "config"

    # Build the managed block contents.
    block_lines: list[str] = [SSH_CONFIG_BEGIN_MARK]
    for n in cfg.nodes:
        if not n.mgmt_ip:
            continue
        canonical = n.name
        lowered = n.name.lower()
        # Both case variants as Host aliases — ssh treats them as
        # alternate names for the same target.
        aliases = canonical if canonical == lowered else f"{canonical} {lowered}"
        block_lines.append(f"Host {aliases}")
        block_lines.append(f"    HostName {n.mgmt_ip}")
        block_lines.append(f"    User {cfg.username}")
        block_lines.append("    StrictHostKeyChecking no")
        block_lines.append("    UserKnownHostsFile /dev/null")
        block_lines.append("")
    block_lines.append(SSH_CONFIG_END_MARK)
    new_block = "\n".join(block_lines) + "\n"

    # Ensure the .ssh directory exists with correct permissions.
    try:
        ssh_config_path.parent.mkdir(mode=0o700, exist_ok=True)
    except Exception as exc:
        console.print(
            f"[warning]Could not create {ssh_config_path.parent}: {exc}[/warning]"
        )
        return

    try:
        existing = ssh_config_path.read_text() if ssh_config_path.is_file() else ""
    except Exception as exc:
        console.print(f"[warning]Could not read {ssh_config_path}: {exc}[/warning]")
        return

    # Replace existing managed block in place, or append if no block yet.
    block_re = re.compile(
        re.escape(SSH_CONFIG_BEGIN_MARK) + r".*?" + re.escape(SSH_CONFIG_END_MARK) + r"\n?",
        re.DOTALL,
    )
    if block_re.search(existing):
        updated = block_re.sub(new_block, existing)
    else:
        sep = "" if existing.endswith("\n") or existing == "" else "\n"
        updated = existing + sep + new_block

    # Skip the write if our block is already in sync with the file content.
    if updated == existing:
        return

    try:
        ssh_config_path.write_text(updated)
        ssh_config_path.chmod(0o600)  # ssh requires restrictive perms on config
    except Exception as exc:
        console.print(
            f"[warning]Could not write {ssh_config_path}: {exc}[/warning] "
            f"Hostname-based SSH may not work in all cases."
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


async def ssh_probe(
    host: str,
    username: str,
    password: str,
    kind: str,
    timeout: float,
) -> Optional[str]:
    """
    Run a real SSH login probe to verify a node is genuinely ready for the
    user — not just "TCP open" but "I can authenticate and run a command."

    The probe uses sshpass for ALL kinds, with kind-specific passwords:

      * arista_ceos: passwordless admin. cEOS's sshd offers keyboard-
                     interactive auth even when the account requires no
                     password — so we can't satisfy it with BatchMode and
                     pure ssh. sshpass with an empty password responds to
                     the prompt and lets us in.

      * linux:       Standard password auth (admin/admin in our labs).
                     sshpass feeds cfg.password.

      * unknown:     Same as cEOS — empty password. Errs on the side of
                     "try the most permissive auth first."

    Returns None on success (we logged in and ran a no-op), or a short
    diagnostic string on failure. Failure strings come from ssh's stderr
    so operators can see *why* — "Could not resolve hostname" indicates
    name resolution is failing, "Connection refused" means sshd isn't
    up yet, etc.
    """
    # Hard-code a per-call connect timeout slightly below the asyncio outer
    # timeout so ssh exits cleanly with stderr instead of getting kill -9'd.
    ssh_connect_timeout = max(1, int(timeout) - 1)

    # All probes run via sshpass → ssh. No BatchMode: sshpass needs to feed
    # a password (or empty string) via the interactive auth flow.
    common_opts = [
        "-o", "StrictHostKeyChecking=no",            # first-boot host keys vary every clab cycle
        "-o", "UserKnownHostsFile=/dev/null",        # don't pollute ~/.ssh/known_hosts
        "-o", "LogLevel=ERROR",                      # mute "Warning: Permanently added" noise
        "-o", "PreferredAuthentications=password,keyboard-interactive,none",
        "-o", "PubkeyAuthentication=no",             # skip key probing — we don't have one
        "-o", f"ConnectTimeout={ssh_connect_timeout}",
    ]

    kind_lc = (kind or "").lower()

    # Kind-specific password and test command:
    #
    #   arista_ceos — empty password + `!` (EOS comment = no-op, exits 0).
    #     cEOS's sshd offers keyboard-interactive even for passwordless admin,
    #     so sshpass feeds an empty string. We can't run `true` because cEOS
    #     hands the command to its CLI parser, not a Unix shell — the parser
    #     rejects it as "% Invalid input" (exit 1).
    #
    #   linux — cfg.password + `true` (standard Unix no-op).
    #
    # Empty password for cEOS is hardcoded (not from cfg.password) because it
    # matches actual cEOS behavior. If a future lab re-enables admin password,
    # the probe fails loudly — which is correct since user SSH would also break.
    if kind_lc == "linux":
        ssh_password = password
        test_command = "true"
    else:
        ssh_password = ""
        test_command = "!"

    # Note: sshpass -p exposes the password in `ps` output. Acceptable here
    # because these are lab-only credentials (admin/admin or empty), not
    # production secrets. For non-lab use, prefer sshpass -e (environment
    # variable) or sshpass -f (file descriptor).
    cmd = [
        "sshpass", "-p", ssh_password,
        "ssh",
        *common_opts,
        f"{username}@{host}",
        test_command,
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

        # Exit 0 = we ran the command on the device. This is the real "ready"
        # signal we want, regardless of node kind.
        if proc.returncode == 0:
            return None

        # Build the failure string from the most useful stderr line — operators
        # need to see WHY the probe failed (resolution issue, refused, etc.).
        meaningful = [ln.strip() for ln in stderr_text.splitlines() if ln.strip()]
        return meaningful[-1] if meaningful else f"ssh exit {proc.returncode}"
    except FileNotFoundError as exc:
        # sshpass or ssh missing from the container. The probe can't proceed;
        # surface a clear message rather than a cryptic traceback.
        return f"required binary missing: {exc.filename or 'sshpass/ssh'}"
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

    Both phases probe by management IP. Hostname-based reachability is a
    user-facing concern handled separately by populate_ssh_config writing
    aliases to ~/.ssh/config.
    """
    node.status = NodeStatus.PROBING_TCP
    node.started_at = time.monotonic()
    deadline = node.started_at + cfg.per_node_timeout

    # We probe by management IP — not hostname — for both phases. In Docker
    # containers, /etc/hosts is bind-mounted and populated late by clab (or
    # not at all for the lab-base container). User-facing hostname ergonomics
    # are handled separately by populate_ssh_config writing aliases to
    # ~/.ssh/config. The probe just answers "is this node's IP reachable?"
    probe_target = node.mgmt_ip or node.name  # prefer IP; fall back to name

    # ── Phase 1: TCP accept ────────────────────────────────────────────────
    while True:
        node.attempts += 1
        err = await tcp_probe(probe_target, cfg.probe_port, DEFAULT_CONNECT_TIMEOUT)
        if err is None:
            break  # port is open — advance to Phase 2
        node.last_error = f"{probe_target}: {err}"

        if time.monotonic() >= deadline:
            node.status = NodeStatus.TIMEOUT
            node.ready_at = time.monotonic()
            return

        await asyncio.sleep(DEFAULT_PROBE_INTERVAL)

    # ── Phase 2: SSH login ────────────────────────────────────────────────
    # TCP is open; now verify we can actually authenticate and run a command.
    node.status = NodeStatus.PROBING_SSH
    node.last_error = None  # clear TCP-phase errors; we're past that

    while True:
        node.attempts += 1

        err = await ssh_probe(
            probe_target, cfg.username, cfg.password, node.kind, DEFAULT_SSH_TIMEOUT
        )
        if err is None:
            node.status = NodeStatus.READY
            node.ready_at = time.monotonic()
            return

        node.last_error = f"{probe_target}: {err}"

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

    readme = cfg.lab_root / "README.md"
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
        NodeStatus.PROBING_SSH:     ("VERIFY SSH LOGIN", "status.probing"),
        NodeStatus.READY:           ("ready",            "status.ready"),
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

    # If nodes have been stuck in SSH phase for a noticeable while, surface the
    # most common error so the operator can see *why* without digging into the
    # failure panel (which only renders after timeout). This is the "why isn't
    # it working" question answered in-flight rather than post-mortem.
    stuck_ssh = [
        n for n in cfg.nodes
        if n.status == NodeStatus.PROBING_SSH and n.last_error and n.elapsed > STUCK_SSH_AGE_SEC
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
        if len(top_err) > DIAG_MSG_MAX_LEN:
            top_err = top_err[:DIAG_MSG_TRUNCATE_AT] + "…"
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


def _render_badge_row(label: str, items: dict) -> list[str]:
    """
    Render a labeled row of pill-shaped key/value badges.

    Used for both the "Validated with" and "Resources" sections of the
    dashboard — same HTML structure, different data. All values pass through
    html.escape so a stray `<` or `&` in lab.yml can't break rendering.
    Returns the lines to append (including the trailing blank line).
    """
    out: list[str] = ['<div class="lab-validated-with">']
    out.append(f'<span class="lab-validated-label">{html.escape(label)}</span>')
    for k, v in items.items():
        out.append(
            f'<span class="lab-badge">'
            f'<span class="lab-badge-key">{html.escape(str(k))}</span>'
            f'<span class="lab-badge-val">{html.escape(str(v))}</span>'
            f'</span>'
        )
    out.append("</div>")
    out.append("")
    return out


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
    # Values pass through html.escape so a malicious lab.yml can't inject
    # markup; not a real concern in the lab use case but cheap defense.
    lines.append('<div class="lab-credentials">')
    lines.append(
        f'<span class="lab-credentials-label">Credentials</span>'
        f'<code class="lab-cred">{html.escape(cfg.username)}</code>'
        f'<span class="lab-cred-sep">/</span>'
        f'<code class="lab-cred">{html.escape(cfg.password)}</code>'
    )
    lines.append("</div>")
    lines.append("")

    # Validated-with badge row — each entry becomes a styled pill.
    if cfg.validated_with:
        lines.extend(_render_badge_row("Validated with", cfg.validated_with))

    # Resources row — same badge styling, different label.
    if cfg.resources:
        lines.extend(_render_badge_row("Resources", cfg.resources))

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

    # ── Node inventory (collapsible) ──
    # The init_lab TUI shows this same data live during boot, so it's not
    # the user's primary view. But after they've moved on from the boot
    # terminal it can still be useful as a hour-2 reference ("what's
    # B-LEAF3's mgmt IP?"). We collapse it by default to keep the
    # dashboard's primary view focused on Quick Actions / Lab Operations,
    # and let the user expand it on demand.
    lines.append("---")
    lines.append("")
    lines.append("<details>")
    lines.append("<summary><strong>🔌 &nbsp; Node Inventory</strong> &nbsp; <sub>(click to expand)</sub></summary>")
    lines.append("")
    lines.append("| Role | Node | Kind | Mgmt IP |")
    lines.append("|------|------|------|---------|")

    def role_sort_key(n: Node) -> tuple[int, str]:
        idx = ROLE_ORDER.index(n.role) if n.role in ROLE_ORDER else 99
        return (idx, n.name)

    for n in sorted(cfg.nodes, key=role_sort_key):
        lines.append(f"| {n.role} | `{n.name}` | {n.kind} | `{n.mgmt_ip or '—'}` |")
    lines.append("")
    lines.append("</details>")
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
        "<sub>Auto-generated by <code>init_lab.py</code> on lab readiness. "
        "Close this tab with <kbd>Ctrl</kbd>+<kbd>W</kbd>.</sub>"
    )
    lines.append("")

    return "\n".join(lines)


def write_and_open_dashboard(cfg: LabConfig, total_elapsed: float, console: Console) -> Optional[Path]:
    """
    Write the dashboard to <lab_root>/LAB-READY.md.

    The PacketAnglers lab-dashboard extension (packetanglers.lab-dashboard)
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
        dash.append(dashboard_path.name, style="bold")
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

    # Pre-flight: write SSH config aliases so the user can `ssh admin@<node>`
    # in either case (canonical or lowercase). We can't reliably populate
    # /etc/hosts in a Docker container — it's bind-mounted from the runtime
    # layer — but ~/.ssh/config is a normal file that ssh honors at the
    # application layer.
    populate_ssh_config(cfg, console)

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


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments for init_lab."""
    parser = argparse.ArgumentParser(
        prog="init_lab.py",
        description=(
            "Lab readiness TUI for Arista Containerized Labs (cArL). "
            "Probes every node in the topology and waits for SSH to be "
            "fully ready before declaring the lab usable. Run from a lab "
            "directory, or use --lab-dir to point at one explicitly."
        ),
    )
    parser.add_argument(
        "--lab-dir",
        type=Path,
        default=None,
        help=(
            "Path to the lab directory (must contain clab/topology.clab.yml "
            "and .vscode/lab.yml). Defaults to the current working directory."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    console = Console(theme=THEME, log_path=False)
    try:
        cfg = load_lab_config(args.lab_dir)
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