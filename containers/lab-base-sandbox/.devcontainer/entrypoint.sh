#!/usr/bin/env bash

set +e

# Start up code-server
if [ -z "${CODE_SERVER_BIND_ADDR}" ]; then
    CODE_SERVER_BIND_ADDR="0.0.0.0:8080"
fi
code-server --bind-addr ${CODE_SERVER_BIND_ADDR} --auth password --disable-telemetry --disable-update-check --disable-workspace-trust "${CONTAINERWSF}" &

# Execute command from docker cli if any.
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
