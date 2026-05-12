ARG FROM_IMAGE

FROM ${FROM_IMAGE}

ARG USERNAME

USER root

# Bake the lab metadata file (lab.yml) and getting-started.md
# into the container image.

COPY ./lab.yml /opt/sandbox/lab.yml
COPY ./getting-started.md /opt/sandbox/getting-started.md
RUN chown -R ${USERNAME}:${USERNAME} /opt/sandbox

# Bake User-level code-server settings into the container image.

COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

# Install the sandbox-dashboard extension.

USER ${USERNAME}

RUN code-server --install-extension PacketAnglers.sandbox-dashboard@0.17.23 --force
