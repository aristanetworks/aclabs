# THIS WILL BE REMOVED ONCE PIVOTED TO MAKING "RESET WORKSPACE" BUTTON
# TO DOWNLOAD TAR OF SANDBOX LAB

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
