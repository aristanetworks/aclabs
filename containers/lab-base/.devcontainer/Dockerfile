# ARG FROM_IMAGE
# ARG FROM_VARIANT
ARG FROM_IMAGE=ghcr.io/aristanetworks/avd/universal
ARG FROM_VARIANT=python3.12-avd-v5.7.2

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

# Create the groups with specific IDs to match your OrbStack host
RUN groupadd -g 2020 docker_host || true && \
    groupadd -r clab_admins || true && \
    usermod -aG 2020,clab_admins ${USERNAME}

# install some basic tools inside the container
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    sshpass \
    iputils-ping \
    htop \
    traceroute \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

# WDion Updates

# Install yq for cli yaml file
RUN apt update \
    && apt autoremove -y \
    && wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_arm64 -O /usr/bin/yq \
    && chmod +x /usr/bin/yq

# install Dependencies
RUN apt-get install -y ca-certificates gnupg && \
    mkdir -p -m 755 /etc/apt/keyrings

# Add the GitHub CLI GPG key
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
    tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg

# Add the GitHub CLI repository
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
    tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Install gh and clean up
RUN apt-get update && \
    apt-get install -y gh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



# copy code-server entrypoint
COPY ./entrypoint.sh /bin/entrypoint
RUN chmod +x /bin/entrypoint
ENTRYPOINT [ "/bin/entrypoint" ]

# copy tasks.json scripts
COPY ./lab_start_task.py /bin/lab_start_task.py
RUN chmod +x /bin/lab_start_task.py

USER ${USERNAME}

# Update pip
RUN pip install --upgrade pip

# Install project requirements
RUN --mount=type=bind,source=/,target=/app/ pip install --user -r /app/requirements.txt
RUN --mount=type=bind,source=/,target=/app/ pip install --user --no-index --find-links=/app/wheelhouse actrac
RUN --mount=type=bind,source=/,target=/app/ ansible-galaxy install -g -f -r /app/requirements.yml


# install the latest containerlab, yamllint, cook-and-cut and eos-downloader
RUN bash -c "$(curl -sL https://get.containerlab.dev)" -- -v ${CLAB_VERSION}

# install coder and extensions
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version="4.106.3" \
    && code-server --install-extension srl-labs.vscode-containerlab --force \
    && code-server --install-extension tuxtina.json2yaml --force \
    && code-server --install-extension yzhang.markdown-all-in-one --force

# --- CUSTOM SHELL CONFIGURATION (Starship, Atuin, Completions) ---

# RUN cat ~/.zshrc >> ~/bak_zshrc

# --- CUSTOM SHELL CONFIGURATION ---

# 1. Install Tools
RUN curl -sS https://starship.rs/install.sh | sh -s -- --yes && \
    curl --proto '=https' --tlsv1.2 -sSf https://setup.atuin.sh | bash -s -- --disable-check-update && \
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# 2. Add our power-user settings to the VERY END of the .zshrc
# This ensures Oh My Zsh doesn't overwrite our arrow key bindings.
RUN echo '\n\
# --- Power User Completion Settings ---\n\
zmodload zsh/complist\n\
autoload -Uz compinit && compinit\n\
\n\
# Standard Emacs-style arrow key bindings\n\
bindkey "^[[A" up-line-or-history    # Up\n\
bindkey "^[[B" down-line-or-history  # Down\n\
bindkey "^[[C" forward-char          # Right\n\
bindkey "^[[D" backward-char         # Left\n\
\n\
# Menu selection navigation\n\
bindkey -M menuselect "^[[A" reverse-menu-complete\n\
bindkey -M menuselect "^[[B" menu-complete\n\
bindkey -M menuselect "^[[C" forward-char\n\
bindkey -M menuselect "^[[D" backward-char\n\
\n\
zstyle ":completion:*" menu select=1\n\
zstyle ":completion:*" matcher-list "m:{a-zA-Z}={A-Za-z}" # Case insensitive\n\
\n\
# App Inits\n\
eval "$(register-python-argcomplete --shell zsh ce_act)"\n\
eval "$(starship init zsh)"\n\
eval "$(atuin init zsh)"' >> ~/.zshrc

# 3. Update plugins
RUN sed -i "s/plugins=(git)/plugins=(git zsh-autosuggestions)/g" ~/.zshrc
RUN echo 'eval "$(gh completion -s zsh)"' >> ~/.zshrc

USER root
# add global workspace settings for code-server
COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

USER ${USERNAME}
