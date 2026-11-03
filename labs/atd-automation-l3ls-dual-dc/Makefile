CURRENT_DIR := $(shell pwd)

.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start
start: build-dci ## Build DCI configurations and deploy the lab
	sudo containerlab deploy --debug --topo $(CURRENT_DIR)/clab/topology.clab.yml --max-workers 10 --timeout 5m --reconfigure

.PHONY: stop
stop: ## Destroy the lab
	sudo containerlab destroy --debug --topo $(CURRENT_DIR)/clab/topology.clab.yml --cleanup

.PHONY: inspect
inspect: ## Inspect the lab
	@sudo containerlab inspect --topo $(CURRENT_DIR)/clab/topology.clab.yml
	@echo ""
	@echo "You can check the lab status, hostnames and management addresses above."
	@echo "To connect to a lab device use \`ssh arista@<hostname>\` and password \`arista\`."

########################################################
# Site 1
########################################################

.PHONY: build-site-1
build-site-1: ## Build Configs
	ansible-playbook playbooks/build.yml -i sites/site_1/inventory.yml -e "target_hosts=SITE1_FABRIC"

.PHONY: deploy-site-1
deploy-site-1: ## Deploy Configs via eAPI
	ansible-playbook playbooks/deploy.yml -i sites/site_1/inventory.yml -e "target_hosts=SITE1_FABRIC"

.PHONY: validate-site-1
validate-site-1: ## Validate network state
	ansible-playbook playbooks/validate.yml -i sites/site_1/inventory.yml -e "target_hosts=SITE1_FABRIC"

########################################################
# Site 2
########################################################

.PHONY: build-site-2
build-site-2: ## Build Configs
	ansible-playbook playbooks/build.yml -i sites/site_2/inventory.yml -e "target_hosts=SITE2_FABRIC"

.PHONY: deploy-site-2
deploy-site-2: ## Deploy Configs via eAPI
	ansible-playbook playbooks/deploy.yml -i sites/site_2/inventory.yml -e "target_hosts=SITE2_FABRIC"

.PHONY: validate-site-2
validate-site-2: ## Validate network state
	ansible-playbook playbooks/validate.yml -i sites/site_2/inventory.yml -e "target_hosts=SITE2_FABRIC"

########################################################
# Build and deploy all sites
########################################################

.PHONY: build-frr
build-frr: ## Generate FRR from existing AVD structured configurations
	ansible-playbook playbooks/build_frr.yml -i localhost,

.PHONY: build-dci
build-dci: ## Build both AVD sites, then generate FRR transport
	$(MAKE) build-site-1
	$(MAKE) build-site-2
	$(MAKE) build-frr

.PHONY: check-frr
check-frr: ## Preview the FRR changes in the running lab
	ansible-playbook playbooks/deploy_frr.yml -i localhost,

.PHONY: deploy-frr
deploy-frr: ## Reconcile and save FRR configuration in the running lab
	ansible-playbook playbooks/deploy_frr.yml -i localhost, -e frr_apply=true

.PHONY: all
all: build-dci ## Build and deploy both sites and FRR in the running lab
	$(MAKE) deploy-frr
	$(MAKE) deploy-site-1
	$(MAKE) deploy-site-2
