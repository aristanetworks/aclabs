ARG FROM_IMAGE

FROM ${FROM_IMAGE}

ARG USERNAME
ARG UID
ARG GID

USER root

# Remap the in-image USERNAME account to the caller-supplied UID/GID so
# bind-mounted workspace files end up owned correctly. The parent image
# ships with the account at UID/GID 1000; we rewrite /etc/passwd and
# /etc/group in place and re-chown the home directory.
ENV OLD_GID="1000"
RUN sed -i -e "s/\(${USERNAME}:[^:]*:\)[^:]*:[^:]*/\1${UID}:${GID}/" /etc/passwd; \
    sed -i -e "s/\([^:]*:[^:]*:\)${OLD_GID}:/\1${GID}:/" /etc/group; \
    chown -R $UID:$GID /home/$USERNAME

# code-server entrypoint — orchestrates code-server launch. Same contract as lab-base.
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

# Install the sandbox-dashboard extension

USER ${USERNAME}

RUN code-server --install-extension PacketAnglers.sandbox-dashboard --force

USER root

# User-level code-server settings

COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

USER ${USERNAME}
