CURRENT_DIR := $(shell pwd)
CLAB_TOPO := $(CURRENT_DIR)/clab/topology.clab.yml
GNMIC_CONTAINER := gnmic

.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start
start: ## Deploy ceos lab
	@test -f $(CURRENT_DIR)/clab/gnmic-mode || printf 'dial-in\n' > $(CURRENT_DIR)/clab/gnmic-mode
	sudo containerlab deploy --debug --topo $(CLAB_TOPO) --max-workers 10 --timeout 5m --reconfigure

.PHONY: stop
stop: ## Destroy ceos lab
	sudo containerlab destroy --debug --topo $(CLAB_TOPO) --cleanup

.PHONY: inspect
inspect: ## Inspect ceos lab
	@sudo containerlab inspect --topo $(CLAB_TOPO)
	@echo ""
	@echo "You can check the lab status, hostnames and management addresses above."
	@echo "To connect to a lab device use \`ssh arista@<hostname>\` and password \`arista\`."

# docker restart cannot change PID 1. Labs started before gnmic-start.sh was
# added still run `/app/gnmic --config gnmic.yml --log subscribe`, so a restart
# never picks up dial-out. Recreate that container from the current topology.
.PHONY: gnmic-apply
gnmic-apply:
	@if docker inspect --format '{{join .Config.Cmd " "}}' $(GNMIC_CONTAINER) 2>/dev/null | grep -q 'gnmic-start.sh'; then \
		echo "Restarting $(GNMIC_CONTAINER) (mode $$(tr -d '[:space:]' < $(CURRENT_DIR)/clab/gnmic-mode))"; \
		docker restart $(GNMIC_CONTAINER); \
	else \
		echo "Recreating $(GNMIC_CONTAINER) from topology.clab.yml so gnmic-start.sh is PID 1"; \
		docker rm -f $(GNMIC_CONTAINER) >/dev/null 2>&1 || true; \
		sudo containerlab deploy --topo $(CLAB_TOPO); \
	fi
	@echo "gNMIc process:"; \
	docker exec $(GNMIC_CONTAINER) ps || true

.PHONY: gnmic-dial-in
gnmic-dial-in: ## Switch gNMIc collector to dial-in (targets on :6030)
	@printf 'dial-in\n' > $(CURRENT_DIR)/clab/gnmic-mode
	@$(MAKE) gnmic-apply
	@echo "gNMIc mode: dial-in"

.PHONY: gnmic-dial-out
gnmic-dial-out: ## Switch gNMIc collector to dial-out (gRPC tunnel server :30000)
	@printf 'dial-out\n' > $(CURRENT_DIR)/clab/gnmic-mode
	@$(MAKE) gnmic-apply
	@echo "gNMIc mode: dial-out"

.PHONY: deploy
deploy: ## Deploy fabric configs with eBGP underlay (default, gNMI dial-in)
	@$(MAKE) gnmic-dial-in
	ansible-playbook playbooks/fabric-deploy-config.yaml

.PHONY: deploy-isis
deploy-isis: ## Deploy fabric configs with IS-IS underlay (gNMI dial-in)
	@$(MAKE) gnmic-dial-in
	ansible-playbook playbooks/fabric-deploy-config.yaml -e underlay_routing_protocol=isis

.PHONY: deploy-dialout
deploy-dialout: ## Deploy fabric configs with eBGP underlay and gNMI dial-out
	@$(MAKE) gnmic-dial-out
	ansible-playbook playbooks/fabric-deploy-config.yaml -e gnmi_dialout=true
