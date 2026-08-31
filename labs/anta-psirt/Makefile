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

.PHONY: psirt-report
psirt-report: ## Run ANTA PSIRT assessment and build a markdown report.
	@anta psirt --ignore-error --ignore-status --username $(ANTA_USERNAME) --password $(ANTA_PASSWORD) --inventory inventory.yml md-report --md-output psirt-report.md
	@/usr/lib/code-server/lib/vscode/bin/remote-cli/code-server -r psirt-report.md

.PHONY: psirt-csv
psirt-csv: ## Run ANTA PSIRT assessment and build a CSV report.
	@anta psirt --ignore-error --ignore-status --username $(ANTA_USERNAME) --password $(ANTA_PASSWORD) --inventory inventory.yml csv --csv-output psirt-report.csv
	@/usr/lib/code-server/lib/vscode/bin/remote-cli/code-server -r psirt-report.csv
