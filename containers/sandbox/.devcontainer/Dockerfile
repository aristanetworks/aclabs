ARG FROM_IMAGE

FROM ${FROM_IMAGE}

ARG USERNAME

USER root

# Bake the lab metadata file (lab.yml) into the container image.

COPY ./lab.yml /opt/lab-base-sandbox/lab.yml
COPY ./getting-started.md /opt/lab-base-sandbox/getting-started.md
RUN chown -R ${USERNAME}:${USERNAME} /opt/lab-base-sandbox

# Install the sandbox-dashboard extension

USER ${USERNAME}

# Ensure the latest version of the extension is always installed.
# Helpful to get around OpenVSX caching issues when iterating through multiple
# versions while testing.
RUN set -eu \
  && LATEST_VSIX=$(curl -fsSL https://api.github.com/repos/PacketAnglers/sandbox-dashboard/releases/latest \
       | grep '"browser_download_url".*\.vsix"' \
       | head -n1 \
       | cut -d'"' -f4) \
  && [ -n "$LATEST_VSIX" ] || { echo "no vsix found in latest release" >&2; exit 1; } \
  && curl -fsSL -o /tmp/sandbox-dashboard.vsix "$LATEST_VSIX" \
  && code-server --install-extension /tmp/sandbox-dashboard.vsix --force \
  && rm /tmp/sandbox-dashboard.vsix

# RUN code-server --install-extension PacketAnglers.sandbox-dashboard --force

USER root

# User-level code-server settings

COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

USER ${USERNAME}
