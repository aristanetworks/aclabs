.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build-deploy-cvp-all
build-deploy-cvp-all: ## Ping Nodes
	make build-domain-a build-domain-b build-domain-c build-backbone deploy-cvp-domain-a deploy-cvp-domain-b deploy-cvp-domain-c deploy-cvp-backbone

.PHONY: deploy-cvp-all
deploy-cvp-all: ## Ping Nodes
	make deploy-cvp-domain-a deploy-cvp-domain-b deploy-cvp-domain-c deploy-cvp-backbone

.PHONY: build-all
build-all: ## Ping Nodes
	make build-domain-a build-domain-b build-domain-c build-backbone

########################################################
# Domain A
########################################################

.PHONY: ping-domain-a
ping-domain-a: ## Ping Nodes
	ansible-playbook playbooks/ping.yml -i domain-a/inventory.yml -e "target_hosts=FABRIC"

.PHONY: build-domain-a
build-domain-a: ## Build Configs
	ansible-playbook playbooks/fabric-build.yml -i domain-a/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-eapi-domain-a
deploy-eapi-domain-a: ## Deploy Configs via eAPI
	ansible-playbook playbooks/fabric-deploy-eapi.yml -i domain-a/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-cvp-domain-a
deploy-cvp-domain-a: ## Deploy Configs via CVP
	ansible-playbook playbooks/fabric-deploy-cvp.yml -i domain-a/inventory.yml

.PHONY: deploy-servers-domain-a
deploy-servers-domain-a: ## Deploy Server Configs via eAPI
	ansible-playbook playbooks/server-deploy-eapi.yml -i domain-a/inventory.yml -e "target_hosts=DOMAIN_A_HOSTS"

########################################################
# Domain B
########################################################

.PHONY: ping-domain-b
ping-domain-b: ## Ping Nodes
	ansible-playbook playbooks/ping.yml -i domain-b/inventory.yml -e "target_hosts=FABRIC"

.PHONY: build-domain-b
build-domain-b: ## Build Configs
	ansible-playbook playbooks/fabric-build.yml -i domain-b/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-eapi-domain-b
deploy-eapi-domain-b: ## Deploy Configs via eAPI
	ansible-playbook playbooks/fabric-deploy-eapi.yml -i domain-b/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-cvp-domain-b
deploy-cvp-domain-b: ## Deploy Configs via CVP
	ansible-playbook playbooks/fabric-deploy-cvp.yml -i domain-b/inventory.yml

.PHONY: deploy-servers-domain-b
deploy-servers-domain-b: ## Deploy Server Configs via eAPI
	ansible-playbook playbooks/server-deploy-eapi.yml -i domain-b/inventory.yml -e "target_hosts=DOMAIN_B_HOSTS"

########################################################
# Domain C
########################################################

.PHONY: ping-domain-c
ping-domain-c: ## Ping Nodes
	ansible-playbook playbooks/ping.yml -i domain-c/inventory.yml -e "target_hosts=FABRIC"

.PHONY: build-domain-c
build-domain-c: ## Build Configs
	ansible-playbook playbooks/fabric-build.yml -i domain-c/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-eapi-domain-c
deploy-eapi-domain-c: ## Deploy Configs via eAPI
	ansible-playbook playbooks/fabric-deploy-eapi.yml -i domain-c/inventory.yml -e "target_hosts=FABRIC"

.PHONY: deploy-cvp-domain-c
deploy-cvp-domain-c: ## Deploy Configs via CVP
	ansible-playbook playbooks/fabric-deploy-cvp.yml -i domain-c/inventory.yml

.PHONY: deploy-servers-domain-c
deploy-servers-domain-c: ## Deploy Server Configs via eAPI
	ansible-playbook playbooks/server-deploy-eapi.yml -i domain-c/inventory.yml -e "target_hosts=DOMAIN_C_HOSTS"

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

.PHONY: deploy-cvp-backbone
deploy-cvp-backbone: ## Deploy Configs via CVP
	ansible-playbook playbooks/fabric-deploy-cvp.yml -i backbone/inventory.yml

########################################################
# Replace domain inventory ansible_hosts with ACT inventory ansible_hosts 
########################################################

.PHONY: replace-domain-a-inventory
replace-domain-a-inventory: 
	python3 scripts/convert_inventory.py domain-a

.PHONY: replace-domain-b-inventory
replace-domain-b-inventory: 
	python3 scripts/convert_inventory.py domain-b

.PHONY: replace-domain-c-inventory
replace-domain-c-inventory: 
	python3 scripts/convert_inventory.py domain-c

.PHONY: replace-backbone-inventory
replace-backbone-inventory: 
	python3 scripts/convert_inventory.py backbone
