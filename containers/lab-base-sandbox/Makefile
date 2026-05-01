# Makefile for lab-base-sandbox container maintenance.
#
# WHY THIS EXISTS
# ───────────────
# The lab-base-sandbox image bakes a "pristine baseline" of the sandbox
# workspace into /opt/sandbox-original/, which the dashboard's Reset
# button uses to restore a known-good state when the user wants to
# start over.
#
# That baseline lab CONTENT (topology.clab.yml, asset images,
# .gitignore) ALSO needs to be available at labs/sandbox/ in this
# repo, because users open the sandbox via a bind mount of
# labs/sandbox/ into /sandbox/ at runtime (see
# .devcontainer/sandbox/devcontainer.json's workspaceMount). The two
# paths must produce the same lab content.
#
# Lab METADATA (lab.yml, README.md) is kept separate. Both files live
# at .devcontainer/{lab.yml,README.md} and are baked into the image
# via their own Dockerfile COPY statements (lab.yml →
# /opt/lab-base-sandbox/lab.yml; README.md → /opt/sandbox-original/
# README.md). They are NOT under labs/sandbox/, so they don't appear
# in the bind-mounted /sandbox/ workspace, and they are NOT under
# .devcontainer/sandbox-original/, so they don't get touched by
# `make sync-baseline`. Metadata is reached via the dashboard's UI
# (Lab Overview card for lab.yml; Getting Started button for
# README.md, using sandbox-dashboard v0.13.0+'s `container://` URL
# scheme).
#
# So this Makefile only manages CONTENT, and the content layout is a
# straight mirror with no special cases:
#
#   labs/sandbox/                    sandbox-original/              /opt/sandbox-original/
#   ────────────────────────────────────────────────────────────────────────────────────
#   topology.clab.yml          ←→   topology.clab.yml          →   topology.clab.yml
#   topology.…annotations.json ←→   topology.…annotations.json →   topology.…annotations.json
#   assets/**                  ←→   assets/**                  →   assets/**
#   .gitignore                 ←→   .gitignore                 →   .gitignore
#
# When labs/sandbox/ content changes, run `make sync-baseline` from
# this directory to copy labs/sandbox/ into
# containers/lab-base-sandbox/.devcontainer/sandbox-original/. Then
# commit both directories together so the next container revision
# picks up the change.
#
# WHY NOT AUTOMATE THIS
# ─────────────────────
# We tried in rev1.0.53 with a CI prebuild hook and a custom workflow
# step. It introduced more failure modes than the manual sync ever
# caused (one drift event in 50+ revisions). Manual is fine.
# Boring solutions for boring problems.

REPO_ROOT := $(shell git rev-parse --show-toplevel)
SOURCE := $(REPO_ROOT)/labs/sandbox
DEST := $(REPO_ROOT)/containers/lab-base-sandbox/.devcontainer/sandbox-original

.PHONY: help sync-baseline check-baseline

help:
	@echo "lab-base-sandbox maintenance targets:"
	@echo ""
	@echo "  make sync-baseline   Copy labs/sandbox/ into sandbox-original/"
	@echo "                       (run when labs/sandbox/ content changes)"
	@echo ""
	@echo "  make check-baseline  Diff labs/sandbox/ against sandbox-original/"
	@echo "                       (no changes; just shows what would be synced)"
	@echo ""

sync-baseline:
	@echo "Syncing $(SOURCE) → $(DEST)"
	@if [ ! -d "$(SOURCE)" ]; then \
	    echo "ERROR: source $(SOURCE) does not exist"; exit 1; \
	fi
	@rm -rf "$(DEST)"
	@mkdir -p "$(DEST)"
	@cp -r "$(SOURCE)/." "$(DEST)/"
	@echo ""
	@echo "Done. Review with:"
	@echo "  git status containers/lab-base-sandbox/.devcontainer/sandbox-original/"
	@echo "  git diff   containers/lab-base-sandbox/.devcontainer/sandbox-original/"
	@echo ""
	@echo "If the sync looks right, commit both labs/sandbox/ and the"
	@echo "sandbox-original/ changes together as part of the next"
	@echo "container revision bump."

check-baseline:
	@echo "Comparing $(SOURCE) vs $(DEST)"
	@if [ ! -d "$(DEST)" ]; then \
	    echo "(sandbox-original/ does not exist yet; run 'make sync-baseline')"; \
	    exit 0; \
	fi
	@diff -rq "$(SOURCE)" "$(DEST)" && echo "✓ in sync" || echo "(differences shown above; run 'make sync-baseline' to update)"
