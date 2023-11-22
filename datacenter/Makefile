.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

########################################################
# Domain A
########################################################

.PHONY: ping-domain-a
ping-domain-a: ## Ping Nodes
	ansible-playbook playbooks/ping.yml -i domain-a/inventory.yml -e "target_hosts=FABRIC"

.PHONY: build-domain-a
build-domain-a: ## Build Configs
	ansible-playbook playbooks/fabric-build.yml -i domain-a/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-domain-a
deploy-domain-a: ## Deploy Configs via eAPI
	ansible-playbook playbooks/fabric-deploy-eapi.yml -i domain-a/inventory.yml -e "target_hosts=FABRIC"

.PHONY: cvp-domain-a
cvp-domain-a: ## Deploy Configs via CVP
	ansible-playbook playbooks/fabric-deploy-cvp.yml -i domain-a/inventory.yml

########################################################
# Domain B
########################################################

.PHONY: ping-domain-b
ping-domain-b: ## Ping Nodes
	ansible-playbook playbooks/ping.yml -i domain-b/inventory.yml -e "target_hosts=FABRIC"

.PHONY: build-domain-b
build-domain-b: ## Build Configs
	ansible-playbook playbooks/fabric-build.yml -i domain-b/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-domain-b
deploy-domain-b: ## Deploy Configs via eAPI
	ansible-playbook playbooks/fabric-deploy-eapi.yml -i domain-b/inventory.yml -e "target_hosts=FABRIC"

.PHONY: cvp-domain-b
cvp-domain-b: ## Deploy Configs via CVP
	ansible-playbook playbooks/fabric-deploy-cvp.yml -i domain-b/inventory.yml

########################################################
# Domain C
########################################################

.PHONY: ping-domain-c
ping-domain-c: ## Ping Nodes
	ansible-playbook playbooks/ping.yml -i domain-c/inventory.yml -e "target_hosts=FABRIC"

.PHONY: build-domain-c
build-domain-c: ## Build Configs
	ansible-playbook playbooks/fabric-build.yml -i domain-c/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-domain-c
deploy-domain-c: ## Deploy Configs via eAPI
	ansible-playbook playbooks/fabric-deploy-eapi.yml -i domain-c/inventory.yml -e "target_hosts=FABRIC"

.PHONY: cvp-domain-c
cvp-domain-c: ## Deploy Configs via CVP
	ansible-playbook playbooks/fabric-deploy-cvp.yml -i domain-c/inventory.yml

########################################################
# BACKBONE
########################################################

.PHONY: ping-backbone
ping-backbone: ## Ping Nodes
	ansible-playbook playbooks/ping.yml -i backbone/inventory.yml -e "target_hosts=FABRIC"

.PHONY: build-backbone
build-backbone: ## Build Configs
	ansible-playbook playbooks/fabric-build.yml -i backbone/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-backbone
deploy-backbone: ## Deploy Configs via eAPI
	ansible-playbook playbooks/fabric-deploy-eapi.yml -i backbone/inventory.yml -e "target_hosts=FABRIC"

.PHONY: cvp-backbone
cvp-backbone: ## Deploy Configs via CVP
	ansible-playbook playbooks/fabric-deploy-cvp.yml -i backbone/inventory.yml
