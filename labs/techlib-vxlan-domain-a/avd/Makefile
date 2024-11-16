.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

########################################################
# Site 1
########################################################

.PHONY: build
build: ## Build Configs
	ansible-playbook playbooks/build.yml -i inventory.yml -e "target_hosts=DOMAIN_A_FABRIC"

.PHONY: deploy
deploy: ## Deploy Configs via eAPI
	ansible-playbook playbooks/deploy.yml -i inventory.yml -e "target_hosts=DOMAIN_A_FABRIC"

.PHONY: validate
validate: ## Validate Fabric
	ansible-playbook playbooks/validate.yml -i inventory.yml -e "target_hosts=DOMAIN_A_FABRIC"
