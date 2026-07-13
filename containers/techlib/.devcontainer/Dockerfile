ARG FROM_IMAGE

FROM ${FROM_IMAGE}

ARG USERNAME

USER root

# Bundled lab scripts. These are the canonical versions used by every
# techlib lab; the lab-dashboard extension resolves /bin/init_lab.py
# before falling back to <workspace>/assets/init_lab.py. init_lab.py
# invokes its sibling docs_generate.py via Path(__file__).parent so
# the pair stays atomic.
COPY ./init_lab.py /bin/init_lab.py
COPY ./docs_generate.py /bin/docs_generate.py
RUN chmod +x /bin/init_lab.py /bin/docs_generate.py

# Bake User-level code-server settings into the container image.

COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

# Install the sandbox-dashboard extension.

USER ${USERNAME}

RUN code-server --install-extension PacketAnglers.lab-dashboard@0.15.4 --force
