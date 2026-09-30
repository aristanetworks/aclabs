ARG FROM_IMAGE

FROM ${FROM_IMAGE}

ARG USERNAME

USER root

# Bundled lab scripts.

COPY ./init_lab.py /bin/init_lab.py
COPY ./docs_generate.py /bin/docs_generate.py

COPY ./lab-deploy.sh /bin/lab-deploy.sh
RUN chmod +x /bin/init_lab.py /bin/docs_generate.py /bin/lab-deploy.sh

# Bake User-level code-server settings into the container image.

COPY ./settings.json /home/${USERNAME}/.local/share/code-server/User
RUN chown ${USERNAME} /home/${USERNAME}/.local/share/code-server/User/settings.json

# Install the lab-dashboard extension. Version is hard coded to better control the environment and avoid unexpected changes.

USER ${USERNAME}

RUN code-server --install-extension PacketAnglers.lab-dashboard@0.15.4 --force
