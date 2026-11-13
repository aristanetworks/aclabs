#!/usr/bin/env python3
"""Display deployment progress and check readiness using SSH authentication only."""

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import time
from typing import Any

import paramiko
import yaml

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text
from rich.theme import Theme


STATE_DIR = Path("/tmp/aclabs-lab-start")
STATE_PATH = STATE_DIR / "state.json"
LOG_PATH = STATE_DIR / "startup.log"
WAIT_TIMEOUT_SECONDS = 900
DEVICE_READY_TIMEOUT_SECONDS = 300
DEVICE_POLL_INTERVAL_SECONDS = 5
DEVICE_USERNAME = os.environ.get("LABUSERNAME") or "arista"
DEVICE_PASSWORD = os.environ.get("LABPASSPHRASE") or "arista"
UI_REFRESH_INTERVAL_SECONDS = 0.25

custom_theme = Theme(
    {"info": "bold cyan", "warning": "magenta", "critical": "bold red"}
)
console = Console(theme=custom_theme, log_path=False)


def show_banner() -> None:
    console.clear()
    console.print("\n\n", end="")

    title = Text()
    title.append("c", style="grey")
    title.append("A", style="red")
    title.append("r", style="green")
    title.append("L", style="bold cyan")
    title.append("\n")

    banner = Text("   ")
    banner.append(title)
    banner.append(Text("   Containerized Arista Labs", style="white"))
    console.print(
        Panel(banner, border_style="cyan", padding=(1, 4), expand=False)
    )
    console.print("\n\n", end="")
    console.print("READ THIS FIRST!", style="critical")
    console.print("- check README.md", style="critical")
    console.print("- wait until the lab is ready", style="critical")
    console.print("\n")


def read_state() -> dict[str, Any]:
    try:
        data: Any = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def topology_nodes(workspace: Path) -> dict[str, str]:
    topology_path = workspace / "clab" / "topology.clab.yml"
    with topology_path.open(encoding="utf-8") as topology_file:
        topology: Any = yaml.safe_load(topology_file)
    nodes = topology["topology"]["nodes"]
    if not isinstance(nodes, dict) or not nodes:
        raise ValueError(f"No lab nodes were found in {topology_path}.")
    return {
        name: (settings or {}).get("mgmt-ipv4", name)
        for name, settings in nodes.items()
    }


def node_is_ready(address: str) -> bool:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=address,
            username=DEVICE_USERNAME,
            password=DEVICE_PASSWORD,
            timeout=3,
            banner_timeout=3,
            auth_timeout=3,
            look_for_keys=False,
            allow_agent=False,
        )
        return True
    except (OSError, EOFError, paramiko.SSHException):
        return False
    finally:
        client.close()


def wait_for_nodes(workspace: Path) -> bool:
    nodes = topology_nodes(workspace)
    unavailable = list(nodes)
    deadline = time.monotonic() + DEVICE_READY_TIMEOUT_SECONDS
    console.log("Lab deployed; waiting for devices to accept SSH...", style="info")

    with console.status(
        f"Waiting for SSH: 0/{len(nodes)} devices ready", spinner="dots"
    ) as progress, ThreadPoolExecutor(max_workers=min(len(nodes), 10)) as executor:
        while time.monotonic() < deadline:
            futures = {
                executor.submit(node_is_ready, nodes[node]): node
                for node in unavailable
            }
            ready_count = len(nodes) - len(unavailable)
            unavailable = []
            for future in as_completed(futures):
                if future.result():
                    ready_count += 1
                else:
                    unavailable.append(futures[future])
                progress.update(
                    f"Waiting for SSH: {ready_count}/{len(nodes)} devices ready"
                )
            if not unavailable:
                console.log("Lab is ready!", style="info")
                return True
            console.print("Waiting for devices: " + ", ".join(sorted(unavailable)))
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(DEVICE_POLL_INTERVAL_SECONDS, remaining))

    console.log(
        f"Devices did not accept SSH within {DEVICE_READY_TIMEOUT_SECONDS} seconds: "
        + ", ".join(sorted(unavailable)),
        style="critical",
    )
    return False


def main() -> int:
    show_banner()
    deadline = time.monotonic() + WAIT_TIMEOUT_SECONDS

    status_text = Text("Waiting for lab startup... ")
    progress = Table.grid(padding=0)
    progress.add_row(status_text, Spinner("dots", style="bold cyan"))
    with Live(progress, console=console, transient=True):
        while time.monotonic() < deadline:
            state = read_state()
            status = state.get("status")

            message = str(state.get("message") or "Waiting for lab startup...")
            status_text.plain = message + " "
            # The shared controller's readiness result requires a remote command.
            # Once deployment finishes, use this task's authentication-only check.
            readiness_failed = status == "FAILED" and message.startswith(
                "ERROR: Devices did not become ready within "
            )
            if status in {"VERIFYING", "READY"} or readiness_failed:
                break
            if status == "FAILED":
                console.log(message, style="critical")
                return 1
            time.sleep(UI_REFRESH_INTERVAL_SECONDS)
        else:
            console.log(
                f"Timed out waiting {WAIT_TIMEOUT_SECONDS} seconds "
                "for automatic lab startup.",
                style="critical",
            )
            return 1

    workspace = Path(__file__).resolve().parents[1]
    try:
        return 0 if wait_for_nodes(workspace) else 1
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as error:
        console.log(f"Failed to check SSH readiness: {error}", style="critical")
        return 1


if __name__ == "__main__":
    exit_code = main()
    if exit_code:
        console.print(f"Startup log: {LOG_PATH}", style="warning")
    raise SystemExit(exit_code)
