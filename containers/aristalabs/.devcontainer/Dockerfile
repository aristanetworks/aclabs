
ARG FROM_IMAGE
ARG FROM_VARIANT

FROM ${FROM_IMAGE}:${FROM_VARIANT}

ARG USERNAME
ARG CLAB_VERSION
ARG GIT_INIT_ARG

USER root

ENV GIT_INIT=${GIT_INIT_ARG}
ENV NEW_UID="1009"
ENV NEW_GID="1009"
ENV OLD_GID="1000"

RUN sed -i -e "s/\(${USERNAME}:[^:]*:\)[^:]*:[^:]*/\1${NEW_UID}:${NEW_GID}/" /etc/passwd; \
    sed -i -e "s/\([^:]*:[^:]*:\)${OLD_GID}:/\1${NEW_GID}:/" /etc/group; \
    chown -R $NEW_UID:$NEW_GID /home/$USERNAME

# install some basic tools inside the container
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    sshpass \
    iputils-ping \
    htop \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

# copy postCreate script
COPY ./postCreate.sh /bin/postCreate.sh
RUN chmod +x /bin/postCreate.sh

# copy code-server entrypoint
COPY ./entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint
ENTRYPOINT [ "/usr/local/bin/entrypoint" ]

USER ${USERNAME}

# install the latest containerlab, yamllint, cook-and-cut and eos-downloader
RUN bash -c "$(curl -sL https://get.containerlab.dev)" -- -v ${CLAB_VERSION} \
    && pip3 install --user yamllint \
    && pip install --user "eos-downloader>=0.10.1" \
    && pip install --user passlib

# install coder and extensions
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version="4.103.1" \
    && code-server --install-extension srl-labs.vscode-containerlab --force \
    && code-server --install-extension tuxtina.json2yaml --force
