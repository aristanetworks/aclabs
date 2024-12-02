#!/usr/bin/env bash

if [ "${GITHUB_REPOSITORY}" ]; then
  grep -rl '{{gh.codespace_name}}' . --exclude-dir .git | xargs sed -i 's/{{gh.repo_name}}/'"${CODESPACE_NAME##*/}"'/g'
  grep -rl '{{gh.codespaces_port_forwarding}}' . --exclude-dir .git | xargs sed -i 's/{{gh.org_name}}/'"${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN%%/*}"'/g'
fi