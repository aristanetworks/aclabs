ARG FROM_IMAGE
ARG FROM_VARIANT

FROM ${FROM_IMAGE}:${FROM_VARIANT}

ARG USERNAME

USER root

ENV NEW_UID="1009"
ENV NEW_GID="1009"
ENV OLD_GID="1000"
RUN sed -i -e "s/\(${USERNAME}:[^:]*:\)[^:]*:[^:]*/\1${NEW_UID}:${NEW_GID}/" /etc/passwd; \
    sed -i -e "s/\([^:]*:[^:]*:\)${OLD_GID}:/\1${NEW_GID}:/" /etc/group; \
    chown -R $NEW_UID:$NEW_GID /home/$USERNAME

# copy code-server entrypoint
COPY ./code-server-entrypoint.sh /usr/local/bin/code-server-entrypoint
RUN chmod +x /usr/local/bin/code-server-entrypoint
ENTRYPOINT [ "/usr/local/bin/code-server-entrypoint" ]

USER ${USERNAME}

# install coder and extensions
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version="4.103.1" \
    && code-server --install-extension srl-labs.vscode-containerlab --force \
    && code-server --install-extension tuxtina.json2yaml --force

# add global workspace settings for code-server
COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown avd /home/${USERNAME}/.local/share/code-server/User/settings.json
