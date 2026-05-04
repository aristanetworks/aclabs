#!/usr/bin/env bash

set +e

if [ -z "${CODE_SERVER_BIND_ADDR}" ]; then
    CODE_SERVER_BIND_ADDR="0.0.0.0:8080"
fi

code-server --bind-addr ${CODE_SERVER_BIND_ADDR} --auth password --disable-telemetry --disable-update-check --disable-workspace-trust "${CONTAINERWSF}" &
