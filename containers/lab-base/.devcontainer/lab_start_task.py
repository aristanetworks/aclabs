#!/usr/bin/env python3
"""Display asynchronous lab startup progress in a VS Code terminal."""

import ipaddress
import json
import os
from pathlib import Path
import time
from typing import Any

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme


STATE_DIR = Path("/tmp/aclabs-lab-start")
STATE_PATH = STATE_DIR / "state.json"
LOG_PATH = STATE_DIR / "startup.log"
TERMINAL_STATES = {"READY", "FAILED"}
WAIT_TIMEOUT_SECONDS = 2400
CVP_EXPECTED_WAIT_SECONDS = 600
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


def print_new_log(offset: int) -> int:
    try:
        with open(LOG_PATH, "r", encoding="utf-8", errors="replace") as log_file:
            log_file.seek(offset)
            output = log_file.read()
            new_offset = log_file.tell()
    except OSError:
        return offset

    if output:
        console.print(output, end="", markup=False)
    return new_offset


ASCII_GLYPHS = {
    "0": (
        " ##### ",
        "##   ##",
        "##   ##",
        "       ",
        "##   ##",
        "##   ##",
        " ##### ",
    ),
    "1": (
        "  ###  ",
        " ####  ",
        "## ##  ",
        "   ##  ",
        "   ##  ",
        "   ##  ",
        "#######",
    ),
    "2": (
        " ##### ",
        "     ##",
        "     ##",
        " ##### ",
        "##     ",
        "##     ",
        " ##### ",
    ),
    "3": (
        " ##### ",
        "     ##",
        "     ##",
        " ##### ",
        "     ##",
        "     ##",
        " ##### ",
    ),
    "4": (
        "       ",
        "##   ##",
        "##   ##",
        " ##### ",
        "     ##",
        "     ##",
        "       ",
    ),
    "5": (
        " ##### ",
        "##     ",
        "##     ",
        " ##### ",
        "     ##",
        "     ##",
        " ##### ",
    ),
    "6": (
        " ##### ",
        "##     ",
        "##     ",
        " ##### ",
        "##   ##",
        "##   ##",
        " ##### ",
    ),
    "7": (
        " ##### ",
        "     ##",
        "     ##",
        "       ",
        "     ##",
        "     ##",
        "       ",
    ),
    "8": (
        " ##### ",
        "##   ##",
        "##   ##",
        " ##### ",
        "##   ##",
        "##   ##",
        " ##### ",
    ),
    "9": (
        " ##### ",
        "##   ##",
        "##   ##",
        " ##### ",
        "     ##",
        "     ##",
        " ##### ",
    ),
    ":": (
        "   ",
        " # ",
        " # ",
        "   ",
        " # ",
        " # ",
        "   ",
    ),
}
BLANK_COLON_GLYPH = ("   ",) * 7


def large_ascii_time(value: str, show_colon: bool) -> list[str]:
    rows = [""] * 7
    for character in value:
        glyph = ASCII_GLYPHS[character]
        if character == ":" and not show_colon:
            glyph = BLANK_COLON_GLYPH
        for index, line in enumerate(glyph):
            separator = "  " if rows[index] else ""
            rows[index] += separator + line
    return rows


def render_watches(countdown: int, frame: int) -> Panel:
    minutes, seconds = divmod(countdown, 60)
    digits = large_ascii_time(
        f"{minutes:02d}:{seconds:02d}",
        show_colon=frame == 0,
    )
    face_width = max(len(line) for line in digits)
    strap = ("|=" if frame == 0 else "=|") * 10
    lines = [
        f"{' ' * 12}{strap}",
        f"      .{'-' * (face_width + 4)}.",
        f"======|{' ' * (face_width + 4)}|======",
    ]
    lines.extend(f"      |  {line:<{face_width}}  |" for line in digits)
    lines.extend(
        (
            f"======|{' ' * (face_width + 4)}|======",
            f"      '{'-' * (face_width + 4)}'",
            f"{' ' * 12}{strap}",
        )
    )
    content = Text("\n".join(lines), style="bold green")
    content.append(
        "\n\nTime left to sacrifice to the CVP API startup demons. ⏳",
        style="yellow",
    )
    return Panel(
        content,
        border_style="green",
        expand=False,
    )


def cvp_wait_animation(started_at: float) -> Panel:
    elapsed = max(0.0, time.time() - started_at)
    remaining = max(0, CVP_EXPECTED_WAIT_SECONDS - int(elapsed))
    frame = int(elapsed * 2) % 2
    if remaining > 0:
        return render_watches(remaining, frame)

    overdue = max(0, int(elapsed) - CVP_EXPECTED_WAIT_SECONDS)
    overdue_minutes, overdue_seconds = divmod(overdue, 60)
    overdue_clock = f"{overdue_minutes:02d}:{overdue_seconds:02d}"

    worried_poses = (
        (
            "    -- O --  ?!  .----------.\n"
            f"       |         |  {overdue_clock}   |\n"
            "      / >        '----------'"
        ),
        (
            "       O__  !!!  .----------.\n"
            f"      <|         |  {overdue_clock}   |\n"
            "      / >        '----------'"
        ),
    )
    animation = Text(worried_poses[frame], style="bold magenta")
    animation.append(
        "\n\nThis is taking longer than expected. "
        "Still waiting until the maximum startup timeout.",
        style="bold yellow",
    )
    return Panel(
        animation,
        title="CloudVision is fashionably late",
        border_style="magenta",
        expand=False,
    )


def main() -> int:
    show_banner()
    deadline = time.monotonic() + WAIT_TIMEOUT_SECONDS
    offset = 0
    wait_live: Live | None = None
    wait_started_at: float | None = None

    try:
        while time.monotonic() < deadline:
            offset = print_new_log(offset)
            state = read_state()
            status = state.get("status")

            if status == "CVP_WAITING":
                if wait_live is None:
                    try:
                        wait_started_at = float(
                            state.get("updated_at", time.time())
                        )
                    except (TypeError, ValueError):
                        wait_started_at = time.time()
                    console.print(str(state.get("message", "Waiting for CVP...")))
                    console.print(
                        "Warning: CloudVision can take up to 10 minutes "
                        "to become available.",
                        style="warning",
                    )
                    wait_live = Live(
                        cvp_wait_animation(wait_started_at),
                        console=console,
                        transient=True,
                        auto_refresh=False,
                    )
                    wait_live.start(refresh=True)
                elif wait_started_at is not None:
                    wait_live.update(
                        cvp_wait_animation(wait_started_at),
                        refresh=True,
                    )
            elif wait_live is not None:
                wait_live.stop()
                wait_live = None
                wait_started_at = None

            if status in TERMINAL_STATES:
                message = str(state.get("message", status))
                if status == "READY":
                    console.log(message, style="info")
                    try:
                        on_prem_cvp = (
                            ipaddress.ip_address(
                                os.environ.get("CVURL", "")
                            ).version
                            == 4
                        )
                    except ValueError:
                        on_prem_cvp = False
                    if on_prem_cvp:
                        console.print(
                            "Open a new terminal to load generated runtime variables.",
                            style="warning",
                        )
                    return 0
                console.log(message, style="critical")
                return 1
            time.sleep(UI_REFRESH_INTERVAL_SECONDS)
    finally:
        if wait_live is not None:
            wait_live.stop()

    console.log(
        f"Timed out waiting {WAIT_TIMEOUT_SECONDS} seconds "
        "for automatic lab startup.",
        style="critical",
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
