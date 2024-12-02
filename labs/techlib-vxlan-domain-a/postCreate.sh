#!/usr/bin/env bash

grep -rl '{{gh.codespace_name}}' . --exclude-dir .git | xargs sed -i 's/{{gh.codespace_name}}/'"${CODESPACE_NAME##*/}"'/g'
grep -rl '{{gh.codespaces_port_forwarding}}' . --exclude-dir .git | xargs sed -i 's/{{gh.codespaces_port_forwarding}}/'"${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN%%/*}"'/g'
