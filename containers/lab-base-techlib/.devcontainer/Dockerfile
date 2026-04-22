# lab-base-techlib
#
# Container image for Arista Tech Library labs on acLabs. Derived from the
# original lab-base Dockerfile with three differences:
#
#   1. Drops /bin/lab_start_task.py — every techlib lab's tasks.json had
#      it commented out, so it's dead weight for this variant.
#   2. Bakes the PacketAnglers lab-dashboard VS Code extension into the
#      code-server install so labs get the dashboard experience without
#      any per-lab bootstrap script.
#   3. Ships init_lab.py and docs_generate.py at /bin/ as the canonical
#      versions for every techlib lab, removing the duplicated-per-lab
#      copies that caused version drift.
#
# Build chain: ghcr.io/aristanetworks/avd/universal:{variant}
#              → lab-base-techlib:{variant}-clab{clab_ver}-rev{rev}[-uid{uid}]

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

# Bundled lab scripts. These are the canonical versions used by every
# techlib lab; the lab-dashboard extension resolves /bin/init_lab.py
# before falling back to <workspace>/assets/init_lab.py. init_lab.py
# invokes its sibling docs_generate.py via Path(__file__).parent so
# the pair stays atomic.
COPY ./init_lab.py /bin/init_lab.py
COPY ./docs_generate.py /bin/docs_generate.py
RUN chmod +x /bin/init_lab.py /bin/docs_generate.py

USER ${USERNAME}

# ContainerLab, plus the Python deps needed by init_lab.py and the AVD
# workflow: yamllint (pre-commit config sanity), eos-downloader (cEOS
# fetch from arista.com), rich + textual (init_lab TUI), passlib (config
# password hashing).
RUN bash -c "$(curl -sL https://get.containerlab.dev)" -- -v ${CLAB_VERSION} \
    && pip3 install --user yamllint \
    && pip install --user "eos-downloader>=0.10.1" \
    && pip install --user rich \
    && pip install --user textual \
    && pip install --user passlib

# code-server + extensions baked in. packetanglers.lab-dashboard is the
# headline addition for this variant — it owns auto-launching init_lab.py
# and rendering LAB-READY.md as an interactive dashboard. Installed from
# Open VSX (code-server's default marketplace). Extensions are pinned to
# minimize the risk of breaking changes.
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

RUN curl -fsSL -o /tmp/lab-dashboard.vsix \
      https://open-vsx.org/api/packetanglers/lab-dashboard/0.14.1/file/packetanglers.lab-dashboard-0.14.1.vsix \
 && code-server --install-extension /tmp/lab-dashboard.vsix --force \
 && rm /tmp/lab-dashboard.vsix

USER root
# User-level code-server settings — applies to every workspace opened
# in this image. workbench.startupEditor=readme + task.allowAutomaticTasks=on
# are both required for the lab-dashboard extension's init_lab launch
# sequencing to work correctly.
COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

USER ${USERNAME}
