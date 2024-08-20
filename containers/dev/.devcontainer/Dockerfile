ARG FROM_IMAGE
ARG FROM_VARIANT

FROM ${FROM_IMAGE}:${FROM_VARIANT}

# Install essential tools.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    curl \
    git-all \
    python3 \
    python3-pip \
    sudo \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

COPY cc.py /bin/cook
RUN chmod +x /bin/cook

ENV TZ=UTC

USER ${USERNAME}

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
