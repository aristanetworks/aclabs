CURRENT_DIR := $(shell pwd)

.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

##################################################
# Containerlab
##################################################

# The topology path is the one thing that differs between techlib labs
# (legacy labs keep it under clab/); the targets below are identical
# across the fleet. start/stop go through /bin/lab-deploy.sh when the
# techlib image provides it (a bounded retry, .lab/deploy.log and
# .lab/deploy.status), and fall back to bare containerlab otherwise.
TOPOLOGY := $(CURRENT_DIR)/topology.clab.yml

.PHONY: start
start: ## Deploy the lab (retries once on a partial deploy; log in .lab/deploy.log)
	@if [ -x /bin/lab-deploy.sh ]; then \
		/bin/lab-deploy.sh deploy $(TOPOLOGY); \
	else \
		sudo containerlab deploy --debug --topo $(TOPOLOGY) --max-workers 10 --timeout 5m --reconfigure; \
	fi

.PHONY: stop
stop: ## Destroy the lab
	@if [ -x /bin/lab-deploy.sh ]; then \
		/bin/lab-deploy.sh destroy $(TOPOLOGY); \
	else \
		sudo containerlab destroy --debug --topo $(TOPOLOGY) --cleanup; \
	fi

.PHONY: inspect
inspect: ## Inspect the lab
	@sudo containerlab inspect --topo $(TOPOLOGY)
	@echo ""
	@echo "You can check the lab status, hostnames and management addresses above."
	@echo "To connect to a lab device use \`ssh admin@<hostname>\` and password \`admin\`."

##################################################
# AVD build / deploy / validate — per-group targets
##################################################

.PHONY: build-a
build-a: ## Build Domain A configs
	ansible-playbook avd/playbooks/build.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_A_FABRIC"

.PHONY: build-b
build-b: ## Build Domain B configs
	ansible-playbook avd/playbooks/build.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_B_FABRIC"

.PHONY: build-bb
build-bb: ## Build Backbone (BB1/BB2) configs
	ansible-playbook avd/playbooks/build.yml -i avd/inventory.yml -e "target_hosts=BACKBONE"

.PHONY: build
build: build-a build-b build-bb ## Build all configs (A + B + Backbone)

.PHONY: deploy-a
deploy-a: ## Deploy Domain A configs via eAPI
	ansible-playbook avd/playbooks/deploy.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_A_FABRIC"

.PHONY: deploy-b
deploy-b: ## Deploy Domain B configs via eAPI
	ansible-playbook avd/playbooks/deploy.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_B_FABRIC"

.PHONY: deploy-bb
deploy-bb: ## Deploy Backbone (BB1/BB2) configs via eAPI
	ansible-playbook avd/playbooks/deploy.yml -i avd/inventory.yml -e "target_hosts=BACKBONE"

.PHONY: deploy
deploy: deploy-a deploy-b deploy-bb ## Deploy all configs (A + B + Backbone)
