CURRENT_DIR := $(shell pwd)

.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start
start: ## Deploy ceos lab
	sudo containerlab deploy --debug --topo $(CURRENT_DIR)/clab/topology.clab.yml --max-workers 10 --timeout 5m --reconfigure

.PHONY: stop
stop: ## Destroy ceos lab
	sudo containerlab destroy --debug --topo $(CURRENT_DIR)/clab/topology.clab.yml --cleanup

.PHONY: inspect
inspect: ## Inspect ceos lab
	@sudo containerlab inspect --topo $(CURRENT_DIR)/clab/topology.clab.yml
	@echo ""
	@echo "You can check the lab status, hostnames and management addresses above."
	@echo "To connect to a lab device use \`ssh admin@<hostname>\` and password \`admin\`."

.PHONY: build
build: ## Build Configs
	ansible-playbook avd/playbooks/build.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_B_FABRIC"

.PHONY: deploy
deploy: ## Deploy Configs via eAPI
	ansible-playbook avd/playbooks/deploy.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_B_FABRIC"

.PHONY: validate
validate: ## Validate Fabric
	ansible-playbook avd/playbooks/validate.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_B_FABRIC"
