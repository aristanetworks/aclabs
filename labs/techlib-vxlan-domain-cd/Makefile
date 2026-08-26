CURRENT_DIR := $(shell pwd)

.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

##################################################
# Containerlab
##################################################

.PHONY: start
start: ## Deploy ceos lab
	sudo containerlab deploy --debug --topo $(CURRENT_DIR)/topology.clab.yml --max-workers 10 --timeout 5m --reconfigure

.PHONY: stop
stop: ## Destroy ceos lab
	sudo containerlab destroy --debug --topo $(CURRENT_DIR)/topology.clab.yml --cleanup

.PHONY: inspect
inspect: ## Inspect ceos lab
	@sudo containerlab inspect --topo $(CURRENT_DIR)/topology.clab.yml
	@echo ""
	@echo "You can check the lab status, hostnames and management addresses above."
	@echo "To connect to a lab device use \`ssh admin@<hostname>\` and password \`admin\`."

##################################################
# AVD build / deploy / validate — per-group targets
##################################################

.PHONY: build-c
build-c: ## Build Domain C configs
	ansible-playbook avd/playbooks/build.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_C_FABRIC"

.PHONY: build-d
build-d: ## Build Domain D configs
	ansible-playbook avd/playbooks/build.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_D_FABRIC"

.PHONY: build-bb
build-bb: ## Build Backbone (BB1/BB2) configs
	ansible-playbook avd/playbooks/build.yml -i avd/inventory.yml -e "target_hosts=BACKBONE"

.PHONY: build
build: build-c build-d build-bb ## Build all configs (C + D + Backbone)

.PHONY: deploy-c
deploy-c: ## Deploy Domain C configs via eAPI
	ansible-playbook avd/playbooks/deploy.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_C_FABRIC"

.PHONY: deploy-d
deploy-d: ## Deploy Domain D configs via eAPI
	ansible-playbook avd/playbooks/deploy.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_D_FABRIC"

.PHONY: deploy-bb
deploy-bb: ## Deploy Backbone (BB1/BB2) configs via eAPI
	ansible-playbook avd/playbooks/deploy.yml -i avd/inventory.yml -e "target_hosts=BACKBONE"

.PHONY: deploy
deploy: deploy-c deploy-d deploy-bb ## Deploy all configs (C + D + Backbone)
