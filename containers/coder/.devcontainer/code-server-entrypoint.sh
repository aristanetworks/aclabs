#!/usr/bin/env bash

set +e

if [ ${LAB_NAME} ]; then
    cd ${CONTAINERWSF}
    wget "https://ankudinov.github.io/aclabs/coder_labs/${LAB_NAME}-coder.tar.gz"
    tar -xzvf ${LAB_NAME}-coder.tar.gz
    rm ${LAB_NAME}-coder.tar.gz
    cp -r ${LAB_NAME}/labs/${LAB_NAME}/. .
    rm -rf ${LAB_NAME}/
fi

code-server --bind-addr 0.0.0.0:8080 --auth password --disable-telemetry --disable-update-check --disable-workspace-trust "${CONTAINERWSF}" &

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
