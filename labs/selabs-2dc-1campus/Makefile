### Generic Variables
SHELL := /bin/zsh

.PHONY: help
help: ## Display help message (*: main entry points / []: part of an entry point)
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

################################################################################
# DC1
################################################################################

.PHONY: dc1-build
dc1-build: ## Run ansible playbook to build DC1 Fabric configuration and documentation
	ansible-playbook playbooks/build.yml -i sites/DC1/inventory.yml -e 'target=DC1'

.PHONY: dc1-deploy_digital_twin_clab
dc1-deploy_digital_twin_clab: ## Run ansible playbook to deploy DC1 on clab Digital Twin Fabric through CVP.
	ansible-playbook playbooks/deploy_digital_twin_clab.yml -i sites/DC1/inventory.yml -e 'target=DC1'

.PHONY: dc1-validate_digital_twin_clab
dc1-validate_digital_twin_clab: ## Validate DC1 sites on clab digital twin
	ansible-playbook playbooks/validate_digital_twin_clab.yml -i sites/DC1/inventory.yml -e 'target=DC1'

################################################################################
# DC2
################################################################################

.PHONY: dc2-build
dc2-build: ## Run ansible playbook to build DC2 Fabric configuration and documentation
	ansible-playbook playbooks/build.yml -i sites/DC2/inventory.yml -e 'target=DC2'

.PHONY: dc2-deploy_digital_twin_clab
dc2-deploy_digital_twin_clab: ## Run ansible playbook to deploy DC2 on clab Digital Twin Fabric through CVP.
	ansible-playbook playbooks/deploy_digital_twin_clab.yml -i sites/DC2/inventory.yml -e 'target=DC2' 

.PHONY: dc2-validate_digital_twin_clab
dc2-validate_digital_twin_clab: ## Validate DC2 site on clab digital twin
	ansible-playbook playbooks/validate_digital_twin_clab.yml -i sites/DC2/inventory.yml -e 'target=DC2'

################################################################################
# Campus
################################################################################

.PHONY: campus-build
campus-build: ## Run ansible playbook to build campus Fabric configuration and documentation
	ansible-playbook playbooks/build.yml -i sites/campus/inventory.yml -e 'target=CAMPUS'

.PHONY: campus-deploy_digital_twin_clab
campus-deploy_digital_twin_clab: ## Run ansible playbook to deploy Campus on clab Digital Twin Fabric through CVP.
	ansible-playbook playbooks/deploy_digital_twin_clab.yml -i sites/campus/inventory.yml -e 'target=CAMPUS' 

.PHONY: campus-validate_digital_twin_clab
campus-validate_digital_twin_clab: ## Validate Campus on clab Digital Twin
	ansible-playbook playbooks/validate_digital_twin_clab.yml -i sites/campus/inventory.yml -e 'target=CAMPUS'

################################################################################
# ALL
################################################################################

.PHONY: build-all
build-all: ## Build all sites
	ansible-playbook playbooks/build.yml -i sites/DC1/inventory.yml -e 'target=DC1'
	ansible-playbook playbooks/build.yml -i sites/DC2/inventory.yml -e 'target=DC2'
	ansible-playbook playbooks/build.yml -i sites/campus/inventory.yml -e 'target=CAMPUS'

.PHONY: deploy-all_digital_twin_clab
deploy-all_digital_twin_clab: ## Deploy all on clab Digital Twin
	ansible-playbook playbooks/deploy_digital_twin_clab.yml -i sites/DC1/inventory.yml -e 'target=DC1'
	ansible-playbook playbooks/deploy_digital_twin_clab.yml -i sites/DC2/inventory.yml -e 'target=DC2'
	ansible-playbook playbooks/deploy_digital_twin_clab.yml -i sites/campus/inventory.yml -e 'target=CAMPUS'

.PHONY: validate-all_clab
validate-all_digital_twin_clab: ## Validate all sites on clab Digital Twin
	-ansible-playbook playbooks/validate_digital_twin_clab.yml -i sites/DC1/inventory.yml -e 'target=DC1'
	-ansible-playbook playbooks/validate_digital_twin_clab.yml -i sites/DC2/inventory.yml -e 'target=DC2'
	-ansible-playbook playbooks/validate_digital_twin_clab.yml -i sites/campus/inventory.yml -e 'target=CAMPUS'

################################################################################
# LAB
################################################################################

.PHONY: get_onboarding_token
get_onboarding_token: ## Generate an onboarding token and save it to file
	ansible-playbook digital_twin/playbooks/get_cvaas_onboarding_token.yml

.PHONY: deploy_clab_topology
deploy_clab_topology: ## Deploy the lab topology on ContainerLab
	clab deploy -t digital_twin/clab/topology.clab.yml

.PHONY: destroy_clab_topology
destroy_clab_topology: ## Destroy the lab topology on ContainerLab
	clab destroy -t digital_twin/clab/topology.clab.yml --cleanup

.PHONY: redeploy_clab_topology
redeploy_clab_topology: ## Destroys and redeploy the clab topology
	clab destroy -t digital_twin/clab/topology.clab.yml --cleanup
	clab deploy -t digital_twin/clab/topology.clab.yml

.PHONY: preplab
preplab: ## Provision _USER_INPUTS.yml, get onboarding token and deploys the lab
	sudo apt update && sudo apt install gh
	ansible-playbook digital_twin/playbooks/user_inputs.yml
	ansible-playbook digital_twin/playbooks/get_cvaas_onboarding_token.yml
	gh auth login
	ansible-playbook digital_twin/playbooks/github_repo.yml
	clab deploy -t digital_twin/clab/topology.clab.yml
