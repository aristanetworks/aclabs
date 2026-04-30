#!/usr/bin/env bash
# Prebuild script for lab-base-sandbox (rev1.0.53+).
#
# Why this exists
# ───────────────
# The lab-base-sandbox image bakes a "pristine baseline" of the sandbox
# workspace into /opt/sandbox-original/, which the dashboard's Reset
# button uses to restore a known-good state when the user wants to
# start over.
#
# That baseline content (topology.clab.yml, README.md, asset images,
# .gitignore) ALSO needs to be available at labs/sandbox/ in this repo,
# because developers who open the aclabs repo directly (via Codespaces
# or devcontainer-cli) get the lab via a bind mount of labs/sandbox/
# rather than from a pre-built image. The two paths must produce the
# same lab.
#
# Pre-rev1.0.53, this was solved by manually duplicating the content
# in `containers/lab-base-sandbox/.devcontainer/sandbox-original/`
# alongside the canonical `labs/sandbox/`. Manual sync introduced
# drift risk — and we hit it with the v0.11.14 dashboard-focused
# README, which only landed in one of the two paths.
#
# rev1.0.53 makes labs/sandbox/ the single source of truth. The
# `containers/.../sandbox-original/` directory becomes a build artifact:
# this script (run by container_build_child.yml before the docker
# build) copies labs/sandbox/ into place. The artifact directory is
# .gitignored so it can never be committed accidentally.
#
# What this does
# ──────────────
#   1. Verifies labs/sandbox/ exists and contains the expected files
#      (fail loudly rather than silently producing an empty baseline).
#   2. Removes any stale sandbox-original/ from prior runs.
#   3. Copies labs/sandbox/ → containers/.../sandbox-original/ verbatim.
#   4. Verifies the copy succeeded by checking key files exist.
#
# Idempotency
# ───────────
# Safe to re-run: removes prior contents before each copy. Local
# developers running docker outside CI should run this manually before
# their build, OR add it as a pre-build hook in their workflow.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SOURCE_DIR="${REPO_ROOT}/labs/sandbox"
DEST_DIR="${REPO_ROOT}/containers/lab-base-sandbox/.devcontainer/sandbox-original"

echo "[prebuild:lab-base-sandbox] repo root:  ${REPO_ROOT}"
echo "[prebuild:lab-base-sandbox] source:     ${SOURCE_DIR}"
echo "[prebuild:lab-base-sandbox] destination: ${DEST_DIR}"

if [ ! -d "${SOURCE_DIR}" ]; then
    echo "[prebuild:lab-base-sandbox] ERROR: ${SOURCE_DIR} does not exist." >&2
    echo "[prebuild:lab-base-sandbox] The lab baseline content must live at labs/sandbox/" >&2
    echo "[prebuild:lab-base-sandbox] in this repo. Cannot proceed without it." >&2
    exit 1
fi

REQUIRED_FILES=(
    "README.md"
    "topology.clab.yml"
)
for f in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "${SOURCE_DIR}/${f}" ]; then
        echo "[prebuild:lab-base-sandbox] ERROR: required file missing: ${SOURCE_DIR}/${f}" >&2
        exit 1
    fi
done

if [ -d "${DEST_DIR}" ]; then
    echo "[prebuild:lab-base-sandbox] removing stale ${DEST_DIR}"
    rm -rf "${DEST_DIR}"
fi

echo "[prebuild:lab-base-sandbox] copying ${SOURCE_DIR} → ${DEST_DIR}"
mkdir -p "${DEST_DIR}"
cp -r "${SOURCE_DIR}/." "${DEST_DIR}/"

for f in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "${DEST_DIR}/${f}" ]; then
        echo "[prebuild:lab-base-sandbox] ERROR: copy verification failed: ${DEST_DIR}/${f}" >&2
        exit 1
    fi
done

echo "[prebuild:lab-base-sandbox] sync complete:"
ls -la "${DEST_DIR}/" | head -20
echo "[prebuild:lab-base-sandbox] done"
