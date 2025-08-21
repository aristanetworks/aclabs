ARG FROM_IMAGE
ARG FROM_VARIANT

FROM ${FROM_IMAGE}:${FROM_VARIANT}

ARG USERNAME

USER root

# install coder and extensions
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version="4.103.1" \
    && code-server --install-extension srl-labs.vscode-containerlab --force \
    && code-server --install-extension tuxtina.json2yaml --force

# copy code-server entrypoint
COPY ./code-server-entrypoint.sh /usr/local/bin/code-server-entrypoint
RUN chmod +x /usr/local/bin/code-server-entrypoint
ENTRYPOINT [ "/usr/local/bin/code-server-entrypoint" ]

USER ${USERNAME}
