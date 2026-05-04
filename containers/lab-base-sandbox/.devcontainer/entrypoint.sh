#!/usr/bin/env bash

set +e

code-server --bind-addr 0.0.0.0:8080 --auth password --disable-telemetry --disable-update-check --disable-workspace-trust "${CONTAINERWSF}" &

if [ ${@+True} ]; then
    exec "$@"
# Otherwise just enter sh or zsh.
else
    if [ -f "/bin/zsh" ]; then
        exec zsh
    else
        exec sh
    fi
fi
