CURRENT_DIR := $(shell pwd)
ANTA_USERNAME ?= "arista"
ANTA_PASSWORD ?= "arista"


.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start
start: ## Deploy the lab
	sudo containerlab deploy --topo $(CURRENT_DIR)/clab/topology.clab.yml --max-workers 4 --timeout 5m --reconfigure

.PHONY: stop
stop: ## Destroy the lab
	sudo containerlab destroy --topo $(CURRENT_DIR)/clab/topology.clab.yml --cleanup

.PHONY: inspect
inspect: ## Inspect the lab
	@sudo containerlab inspect --topo $(CURRENT_DIR)/clab/topology.clab.yml

.PHONY: sat-report
sat-report: ## Run ANTA security advisory tests and build a markdown report.
	@anta sat --ignore-error --ignore-status --username $(ANTA_USERNAME) --password $(ANTA_PASSWORD) --inventory inventory.yml md-report --md-output sat-report.md
	@/usr/lib/code-server/lib/vscode/bin/remote-cli/code-server -r sat-report.md

.PHONY: sat-report-expanded
sat-report-expanded: ## Run ANTA security advisory tests and build an expanded markdown report.
	@anta sat --ignore-error --ignore-status --username $(ANTA_USERNAME) --password $(ANTA_PASSWORD) --inventory inventory.yml md-report --md-output sat-report-expanded.md --expand
	@/usr/lib/code-server/lib/vscode/bin/remote-cli/code-server -r sat-report-expanded.md

.PHONY: sat-csv
sat-csv: ## Run ANTA security advisory tests and build a CSV report.
	@anta sat --ignore-error --ignore-status --username $(ANTA_USERNAME) --password $(ANTA_PASSWORD) --inventory inventory.yml csv --csv-output sat-report.csv
	@/usr/lib/code-server/lib/vscode/bin/remote-cli/code-server -r sat-report.csv
