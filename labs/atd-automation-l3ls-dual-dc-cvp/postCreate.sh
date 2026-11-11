#!/usr/bin/env bash

set -euo pipefail

# Trust the mounted lab repository even when GIT_INIT is disabled.
# TODO: Remove this workaround once the main entrypoint sets safe.directory regardless of GIT_INIT.
git config --global --add safe.directory "${CONTAINERWSF}"

# License acceptance must be in code-server user settings, not workspace settings.
settings_file="$HOME/.local/share/code-server/User/settings.json"
jq '.["arista-avd-yaml.eulaAccepted"] = true' \
    "$settings_file" > "${settings_file}.tmp"
mv -- "${settings_file}.tmp" "$settings_file"

ansible-galaxy collection install community.docker

# Discover the supplied extension without hardcoding its version.
shopt -s nullglob
vsix_files=("${CONTAINERWSF}"/arista-avd-yaml-*.vsix)

if (( ${#vsix_files[@]} != 1 )); then
    echo "Expected exactly one arista-avd-yaml-*.vsix in ${CONTAINERWSF}" >&2
    exit 1
fi

code-server --install-extension "${vsix_files[0]}" --force
rm -- "${vsix_files[0]}"

code-server --install-extension samuelcolvin.jinjahtml --force
