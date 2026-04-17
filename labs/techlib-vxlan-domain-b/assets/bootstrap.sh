#!/bin/sh
# bootstrap.sh — Ensure the lab-dashboard extension is installed.
#
# Triggered by .vscode/tasks.json on folderOpen. Installs the PacketAnglers
# lab-dashboard extension if it isn't already present. Once installed,
# the extension activates and handles everything else:
#
#   * Auto-launches assets/init_lab.py (boot TUI, node probes, SSH config)
#   * Watches for LAB-READY.md and opens the dashboard webview
#   * Provides the status bar button, topology viewer, terminal commands
#
# Idempotent: if the extension is already installed, this completes in
# ~200ms and the extension activates normally.

set -eu

EXTENSION_ID="packetanglers.lab-dashboard"

if ! command -v code-server >/dev/null 2>&1; then
    echo "[bootstrap] code-server not found — skipping extension install" >&2
    exit 0
fi

if code-server --list-extensions 2>/dev/null | grep -qi "${EXTENSION_ID}"; then
    echo "[bootstrap] lab-dashboard extension already installed"
else
    echo "[bootstrap] Installing ${EXTENSION_ID}..."
    code-server --install-extension "${EXTENSION_ID}" --force 2>&1 | tail -1
    echo "[bootstrap] Installed — extension activating"
fi
