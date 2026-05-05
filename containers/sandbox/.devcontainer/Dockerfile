ARG FROM_IMAGE

FROM ${FROM_IMAGE}

ARG USERNAME

USER root

# Bake the lab metadata file (lab.yml) into the container image.

COPY ./lab.yml /opt/lab-base-sandbox/lab.yml
RUN chown -R ${USERNAME}:${USERNAME} /opt/lab-base-sandbox

# Install the sandbox-dashboard extension

USER ${USERNAME}

RUN code-server --install-extension PacketAnglers.sandbox-dashboard --force

USER root

# User-level code-server settings

COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

USER ${USERNAME}
