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

.PHONY: validate-a
validate-a: ## Run ANTA tests against Domain A
	ansible-playbook avd/playbooks/validate.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_A_FABRIC"

.PHONY: validate-b
validate-b: ## Run ANTA tests against Domain B
	ansible-playbook avd/playbooks/validate.yml -i avd/inventory.yml -e "target_hosts=DOMAIN_B_FABRIC"

.PHONY: validate-bb
validate-bb: ## Run ANTA tests against Backbone (BB1/BB2)
	ansible-playbook avd/playbooks/validate.yml -i avd/inventory.yml -e "target_hosts=BACKBONE"

.PHONY: validate
validate: validate-a validate-b validate-bb ## Run ANTA tests against everything (A + B + Backbone)

##################################################
# Config parity check — diff rendered vs. tech-library reference
#
# TECHLIB env var must point at the tech-library repo root.
# Example: `TECHLIB=~/repos/tech-library make diff-a`
##################################################

TECHLIB_CFG := $(TECHLIB)/docs/data_center/evpnvxlan/deployment_guide/domains_a_b/full_configs
RENDERED    := $(CURRENT_DIR)/avd/intended/configs

.PHONY: diff-a
diff-a: ## Diff Domain A rendered configs vs. tech-library reference (requires TECHLIB=...)
	@for h in A-SPINE1 A-SPINE2 A-SPINE3 A-SPINE4 A-LEAF1 A-LEAF2 A-LEAF3 A-LEAF4 A-LEAF5 A-LEAF6 A-LEAF7 A-LEAF8; do \
		echo "=== $$h ==="; \
		diff -u $(RENDERED)/$$h.cfg $(TECHLIB_CFG)/$$h.cfg || true; \
	done

.PHONY: diff-b
diff-b: ## Diff Domain B rendered configs vs. tech-library reference (requires TECHLIB=...)
	@for h in B-SPINE1 B-SPINE2 B-SPINE3 B-SPINE4 B-LEAF1 B-LEAF2 B-LEAF3 B-LEAF4 B-LEAF5 B-LEAF6 B-LEAF7 B-LEAF8 B-SW1; do \
		echo "=== $$h ==="; \
		diff -u $(RENDERED)/$$h.cfg $(TECHLIB_CFG)/$$h.cfg || true; \
	done

.PHONY: diff-bb
diff-bb: ## Diff Backbone rendered configs vs. tech-library reference (requires TECHLIB=...)
	@for h in BB1 BB2; do \
		echo "=== $$h ==="; \
		diff -u $(RENDERED)/$$h.cfg $(TECHLIB_CFG)/$$h.cfg || true; \
	done

.PHONY: diff
diff: diff-a diff-b diff-bb ## Diff everything vs. tech-library reference (requires TECHLIB=...)
