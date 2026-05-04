# lab-base-sandbox
#
# Container image for the UCN Sandbox lab on acLabs. Built from the `lab-base`
# image found on acLabs.

ARG FROM_IMAGE

FROM ${FROM_IMAGE}

ARG USERNAME

USER root

# code-server entrypoint — orchestrates cEOS image load, config token
# generation, and code-server launch. Same contract as lab-base.
COPY ./entrypoint.sh /bin/entrypoint
RUN chmod +x /bin/entrypoint
ENTRYPOINT [ "/bin/entrypoint" ]

# Maintain files from labs/sandbox in the container so that they
# can be used for `reset` operations.

COPY ./sandbox-original/ /opt/sandbox-original/
RUN chown -R ${USERNAME}:${USERNAME} /opt/sandbox-original

# Bake the lab metadata file (lab.yml) into the container image.

COPY ./lab.yml /opt/lab-base-sandbox/lab.yml
RUN chown -R ${USERNAME}:${USERNAME} /opt/lab-base-sandbox

# User-level code-server settings

COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

# Install the sandbox-dashboard extension

USER ${USERNAME}

RUN code-server --install-extension PacketAnglers.sandbox-dashboard --force

USER ${USERNAME}
