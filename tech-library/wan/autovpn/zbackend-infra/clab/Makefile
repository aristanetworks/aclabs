.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: push-configs
push-configs: ## Push configs to lab
	ansible-playbook config_push.yml

.PHONY: grab-configs
grab-configs: ## Grab configs from the lab
	ansible-playbook config_grab.yml

.PHONY: push-license
push-license: ## Push license to CloudEOS nodes
	pip3 install paramiko ansible-pylibssh
	ansible-playbook push_license.yml -e ansible_connection=network_cli
