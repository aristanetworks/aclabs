#!/usr/bin/env python3
"""
docs_generate.py — Regenerate README.md managed blocks from lab.yml + shared snippets.

Treats the README as a hybrid document: human-authored prose PLUS blocks of content
that are generated from canonical sources. The managed blocks are delimited by HTML
comment markers; everything outside them is preserved verbatim.

Two marker styles are supported:

  <!-- lab-dashboard:metadata-start -->
  ...content generated from .vscode/lab.yml...
  <!-- lab-dashboard:metadata-end -->

  <!-- lab-dashboard:snippet <name> -->
  ...content inlined from ../_shared/snippets/<name>.md...
  <!-- lab-dashboard:snippet-end -->

Usage:
  python3 .vscode/docs_generate.py           # Rewrite README.md in place
  python3 .vscode/docs_generate.py --check   # Exit non-zero if README would change
  python3 .vscode/docs_generate.py --diff    # Show what would change without writing

Exit codes:
  0 — README is (now) up to date
  1 — (--check only) README is out of sync
  2 — Structural error (missing markers, missing snippet file, malformed lab.yml)

The script is idempotent: running it twice in a row produces identical output.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import Optional

import yaml


# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

LAB_YML_PATH = Path(".vscode/lab.yml")
README_PATH = Path("README.md")

# Shared snippets live at labs/_shared/snippets/ — two levels up from a lab dir.
SHARED_SNIPPETS_DIR = Path("../_shared/snippets")

# Markers. The snippet-start regex captures the snippet name as group 1.
METADATA_START = "<!-- lab-dashboard:metadata-start -->"
METADATA_END = "<!-- lab-dashboard:metadata-end -->"
METADATA_BLOCK_RE = re.compile(
    re.escape(METADATA_START) + r"(.*?)" + re.escape(METADATA_END),
    re.DOTALL,
)
SNIPPET_BLOCK_RE = re.compile(
    r"<!--\s*lab-dashboard:snippet\s+([A-Za-z0-9_-]+)\s*-->"
    r"(.*?)"
    r"<!--\s*lab-dashboard:snippet-end\s*-->",
    re.DOTALL,
)


# ─────────────────────────────────────────────────────────────────────────────
# Metadata block rendering
# ─────────────────────────────────────────────────────────────────────────────

# Valid GitHub alert types. See:
# https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/basic-writing-and-formatting-syntax#alerts
VALID_BANNER_TYPES = {"note", "tip", "important", "warning", "caution"}


def render_banner(banner: Optional[dict]) -> list[str]:
    """
    Render a banner block from the `display.banner` section of lab.yml.

    Returns lines to emit (without a trailing blank), or an empty list when
    the banner is omitted. Raises ValueError for malformed banner configs —
    those are authoring mistakes that should fail loudly, not silently.
    """
    if not banner:
        return []

    if not isinstance(banner, dict):
        raise ValueError(
            f"display.banner must be a mapping with 'type' and 'message' keys, "
            f"got {type(banner).__name__}"
        )

    banner_type = str(banner.get("type", "")).strip().lower()
    message = banner.get("message", "").strip()

    if banner_type not in VALID_BANNER_TYPES:
        raise ValueError(
            f"display.banner.type must be one of "
            f"{sorted(VALID_BANNER_TYPES)}, got '{banner_type}'"
        )
    if not message:
        raise ValueError("display.banner.message must be a non-empty string")

    # GitHub alert syntax: > [!TYPE] on its own line, then > message lines.
    # Preserve author line breaks in the message by prefixing each with '> '.
    lines = [f"> [!{banner_type.upper()}]"]
    for msg_line in message.splitlines() or [message]:
        lines.append(f"> {msg_line}".rstrip())
    return lines


# ─────────────────────────────────────────────────────────────────────────────
# Metadata block rendering
# ─────────────────────────────────────────────────────────────────────────────

def render_metadata_block(lab_yml: dict) -> str:
    """
    Build the metadata block that sits at the top of every lab README.

    Contains the lab-identifying facts that are canonical in lab.yml:
      - Lab title
      - Subtitle (italicized)
      - Optional banner (WARNING / NOTE / etc. — omit for none)
      - Documentation URL
      - Credentials

    Deliberately EXCLUDED (per design decision):
      - Validated-with versions / resources — dashboard-only
      - Node inventory — dashboard-only
    """
    display = lab_yml.get("display", {}) or {}
    credentials = lab_yml.get("credentials", {}) or {}

    title = display.get("name", "Unnamed Lab")
    subtitle = display.get("subtitle")
    doc_url = display.get("documentation_url")
    username = credentials.get("username", "admin")
    password = credentials.get("password", "admin")

    lines: list[str] = []
    lines.append("")  # blank line after start marker for readability
    lines.append(f"# {title}")
    lines.append("")

    if subtitle:
        lines.append(f"_{subtitle}_")
        lines.append("")

    banner_lines = render_banner(display.get("banner"))
    if banner_lines:
        lines.extend(banner_lines)
        lines.append("")

    if doc_url:
        lines.append(
            f"📖 **Deployment Guide:** [Tech Library]({doc_url})"
        )
        lines.append("")

    lines.append("🔐 **Credentials**")
    lines.append("")
    lines.append(f"| Username | Password |")
    lines.append(f"|----------|----------|")
    lines.append(f"| `{username}` | `{password}` |")
    lines.append("")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Snippet loading
# ─────────────────────────────────────────────────────────────────────────────

def load_snippet(name: str, lab_dir: Path) -> str:
    """
    Load a shared snippet by name. Resolves to labs/_shared/snippets/<name>.md.

    Raises FileNotFoundError with a helpful message if the snippet is missing.
    """
    snippet_path = (lab_dir / SHARED_SNIPPETS_DIR / f"{name}.md").resolve()
    if not snippet_path.is_file():
        raise FileNotFoundError(
            f"Snippet '{name}' not found at expected path: {snippet_path}\n"
            f"Available snippets:\n  "
            + "\n  ".join(
                sorted(
                    p.stem for p in (lab_dir / SHARED_SNIPPETS_DIR).glob("*.md")
                )
                if (lab_dir / SHARED_SNIPPETS_DIR).is_dir()
                else ["(snippets directory not found)"]
            )
        )
    content = snippet_path.read_text()
    # Normalize trailing whitespace. Ensure exactly one leading + trailing blank
    # line inside the block for consistent rendering regardless of source file.
    stripped = content.strip("\n")
    return f"\n{stripped}\n"


# ─────────────────────────────────────────────────────────────────────────────
# README regeneration
# ─────────────────────────────────────────────────────────────────────────────

def regenerate_readme(readme_content: str, lab_yml: dict, lab_dir: Path) -> str:
    """
    Rewrite all managed blocks in README content. Pure function — doesn't touch disk.

    Preserves everything outside the markers byte-for-byte.
    """
    # 1. Metadata block. Must be present — it's the lab identity.
    if not METADATA_BLOCK_RE.search(readme_content):
        raise ValueError(
            f"README is missing the metadata markers. Please add:\n\n"
            f"    {METADATA_START}\n"
            f"    {METADATA_END}\n\n"
            f"at the top of the file (both markers required, even if currently empty)."
        )

    new_metadata = render_metadata_block(lab_yml)
    readme_content = METADATA_BLOCK_RE.sub(
        lambda _m: f"{METADATA_START}\n{new_metadata}\n{METADATA_END}",
        readme_content,
        count=1,
    )

    # 2. Snippet blocks. Each match gets its content replaced with the live snippet.
    def replace_snippet(match: re.Match) -> str:
        name = match.group(1)
        body = load_snippet(name, lab_dir)
        return (
            f"<!-- lab-dashboard:snippet {name} -->"
            f"{body}"
            f"<!-- lab-dashboard:snippet-end -->"
        )

    readme_content = SNIPPET_BLOCK_RE.sub(replace_snippet, readme_content)

    return readme_content


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate README.md managed blocks from lab.yml + shared snippets.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if README would change. Use in CI.",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Print a unified diff of proposed changes without writing.",
    )
    parser.add_argument(
        "--lab-dir",
        type=Path,
        default=Path.cwd(),
        help="Lab directory (default: current working directory).",
    )
    args = parser.parse_args(argv)

    lab_dir: Path = args.lab_dir.resolve()
    lab_yml_path = lab_dir / LAB_YML_PATH
    readme_path = lab_dir / README_PATH

    # ── Validate inputs ──
    # docs_generate.py lives in /bin and operates on whatever lab dir it was
    # pointed at. Give a clear message if the dir doesn't look right rather
    # than a one-line "file not found" that leaves the user guessing.
    missing = []
    if not lab_yml_path.is_file():
        missing.append(f".vscode/lab.yml (expected at {lab_yml_path})")
    if not readme_path.is_file():
        missing.append(f"README.md (expected at {readme_path})")
    if missing:
        source = (
            "(from --lab-dir)"
            if args.lab_dir != Path.cwd()
            else f"(from current working directory: {Path.cwd()})"
        )
        print(
            f"error: not a valid lab directory: {lab_dir} {source}",
            file=sys.stderr,
        )
        for m in missing:
            print(f"  - missing: {m}", file=sys.stderr)
        print(
            "tip: cd into a lab directory and re-run, or use:\n"
            "  docs_generate.py --lab-dir /path/to/lab",
            file=sys.stderr,
        )
        return 2

    try:
        with lab_yml_path.open() as f:
            lab_yml = yaml.safe_load(f) or {}
    except yaml.YAMLError as exc:
        print(f"error: failed to parse {lab_yml_path}: {exc}", file=sys.stderr)
        return 2

    original = readme_path.read_text()
    try:
        updated = regenerate_readme(original, lab_yml, lab_dir)
    except (ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # ── Decide what to do with the result ──
    if original == updated:
        if not args.check and not args.diff:
            print(f"{readme_path.name} is already up to date.")
        return 0

    if args.diff:
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=f"{readme_path.name} (current)",
            tofile=f"{readme_path.name} (regenerated)",
        )
        sys.stdout.writelines(diff)
        return 0

    if args.check:
        print(
            f"error: {readme_path.name} is out of sync with {lab_yml_path.name}.\n"
            f"       Run `python3 .vscode/docs_generate.py` to regenerate.",
            file=sys.stderr,
        )
        return 1

    readme_path.write_text(updated)
    print(f"Regenerated {readme_path.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
