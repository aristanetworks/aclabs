ARG FROM_IMAGE
ARG FROM_VARIANT

FROM ${FROM_IMAGE}:${FROM_VARIANT}

ARG USERNAME

USER root

# install coder and extensions
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version="4.103.1" \
    && code-server --install-extension srl-labs.vscode-containerlab --force \
    && code-server --install-extension tuxtina.json2yaml --force
    # && code-server --bind-addr 127.0.0.1:8080 --auth password --disable-telemetry --disable-update-check --disable-workspace-trust "/cvaas-cvaas-and-avd-demo--evpn-mlag"

USER ${USERNAME}
