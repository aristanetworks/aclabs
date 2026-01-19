ARG FROM_IMAGE
ARG FROM_VARIANT

FROM ${FROM_IMAGE}:${FROM_VARIANT}

ARG USERNAME
ARG CLAB_VERSION
ARG CEOS_LAB_VERSION_ARG
ARG GIT_INIT_ARG
ARG UID
ARG GID

ENV CEOS_LAB_VERSION=${CEOS_LAB_VERSION_ARG}
ENV GIT_INIT=${GIT_INIT_ARG}

USER root

ENV OLD_GID="1000"
RUN sed -i -e "s/\(${USERNAME}:[^:]*:\)[^:]*:[^:]*/\1${UID}:${GID}/" /etc/passwd; \
    sed -i -e "s/\([^:]*:[^:]*:\)${OLD_GID}:/\1${GID}:/" /etc/group; \
    chown -R $UID:$GID /home/$USERNAME

# install some basic tools inside the container
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    sshpass \
    iputils-ping \
    htop \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

# copy code-server entrypoint
COPY ./entrypoint.sh /bin/entrypoint
RUN chmod +x /bin/entrypoint
ENTRYPOINT [ "/bin/entrypoint" ]

# copy tasks.json scripts
COPY ./lab_start_task.py /bin/lab_start_task.py
RUN chmod +x /bin/lab_start_task.py

USER ${USERNAME}

# install the latest containerlab, yamllint, cook-and-cut and eos-downloader
RUN bash -c "$(curl -sL https://get.containerlab.dev)" -- -v ${CLAB_VERSION} \
    && pip3 install --user yamllint \
    && pip install --user "eos-downloader>=0.10.1" \
    && pip install --user rich \
    && pip install --user passlib

# install coder and extensions
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version="4.106.3" \
    && code-server --install-extension srl-labs.vscode-containerlab --force \
    && code-server --install-extension tuxtina.json2yaml --force \
    && code-server --install-extension yzhang.markdown-all-in-one --force

USER root
# add global workspace settings for code-server
COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

USER ${USERNAME}
