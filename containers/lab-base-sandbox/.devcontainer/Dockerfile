# lab-base-sandbox
#
# Container image for the UCN Sandbox lab on acLabs. Sister image to
# lab-base-techlib — shares the same OS layer, code-server, ContainerLab,
# and supporting Python deps, but differs in two ways:
#
#   1. Bakes the PacketAnglers sandbox-dashboard VS Code extension instead
#      of lab-dashboard. Sandbox is a stateful long-lived control plane
#      (import / start / save / export); techlib is a write-once status
#      renderer. Different jobs, different extensions.
#   2. Does NOT ship /bin/init_lab.py or /bin/docs_generate.py. The
#      sandbox lab doesn't auto-deploy a topology — the user drives the
#      lifecycle from the sandbox-dashboard webview, so there's nothing
#      for an init_lab script to wait for at boot.
#
# Build chain: ghcr.io/aristanetworks/avd/universal:{variant}
#              → lab-base-sandbox:{variant}-clab{clab_ver}-rev{rev}[-uid{uid}]

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

# Remap the in-image USERNAME account to the caller-supplied UID/GID so
# bind-mounted workspace files end up owned correctly. The parent image
# ships with the account at UID/GID 1000; we rewrite /etc/passwd and
# /etc/group in place and re-chown the home directory.
ENV OLD_GID="1000"
RUN sed -i -e "s/\(${USERNAME}:[^:]*:\)[^:]*:[^:]*/\1${UID}:${GID}/" /etc/passwd; \
    sed -i -e "s/\([^:]*:[^:]*:\)${OLD_GID}:/\1${GID}:/" /etc/group; \
    chown -R $UID:$GID /home/$USERNAME

# Minimal apt layer: sshpass for non-interactive SSH to lab nodes,
# iputils-ping for basic reachability testing, htop for process
# inspection during debugging.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    sshpass \
    iputils-ping \
    htop \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

# code-server entrypoint — orchestrates cEOS image load, config token
# generation, and code-server launch. Same contract as lab-base.
COPY ./entrypoint.sh /bin/entrypoint
RUN chmod +x /bin/entrypoint
ENTRYPOINT [ "/bin/entrypoint" ]

USER ${USERNAME}

# ContainerLab, plus the Python deps that match lab-base-techlib for env
# parity (yamllint for YAML editing, eos-downloader for cEOS image fetch
# from arista.com, rich + textual for any TUI work in future helper
# scripts, passlib for config password hashing if needed).
RUN bash -c "$(curl -sL https://get.containerlab.dev)" -- -v ${CLAB_VERSION} \
    && pip3 install --user yamllint \
    && pip install --user "eos-downloader>=0.10.1" \
    && pip install --user rich \
    && pip install --user textual \
    && pip install --user passlib

# code-server + extensions baked in. packetanglers.sandbox-dashboard is the
# headline addition for this variant — it owns the sandbox lab lifecycle
# UI (import / start / save / export). Installed from Open VSX
# (code-server's default marketplace). Extensions are pinned to minimize
# the risk of breaking changes.
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version="4.115.0"

RUN for ext in \
        srl-labs.vscode-containerlab@0.24.2 \
        tuxtina.json2yaml@0.2.0 \
        yzhang.markdown-all-in-one@3.6.2; do \
        echo ">> installing $ext"; \
        for attempt in 1 2 3; do \
            code-server --install-extension "$ext" --force && break; \
            echo ">> attempt $attempt failed for $ext"; \
            [ "$attempt" = "3" ] && echo ">> FATAL: $ext failed after 3 attempts" && exit 1; \
            sleep $((attempt * 5)); \
        done; \
    done

RUN curl -fsSL -o /tmp/sandbox-dashboard.vsix \
      https://open-vsx.org/api/packetanglers/sandbox-dashboard/0.8.0/file/packetanglers.sandbox-dashboard-0.8.0.vsix \
 && code-server --install-extension /tmp/sandbox-dashboard.vsix --force \
 && rm /tmp/sandbox-dashboard.vsix

USER root
# User-level code-server settings — applies to every workspace opened
# in this image. Suppresses the Welcome tab and the Red Hat YAML
# telemetry consent popup so users land in a clean workspace ready
# to drive the sandbox-dashboard webview.
COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

USER ${USERNAME}
