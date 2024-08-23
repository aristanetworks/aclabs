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
    # TODO: have to review the bottom part later
    ca-certificates \
    cdpr \
    dnsutils \
    dsniff \
    ipcalc \
    iperf \
    iperf3 \
    fping \
    gnupg \
    gsutil \
    ifenslave \
    inetutils-traceroute \
    iputils-* \
    libkrb5-dev \
    lldpd \
    locales \
    mtr \
    nano \
    net-tools \
    netplan.io \
    openssh-server \
    snapd \
    tzdata \
    ufw \
    vim
    # no need to reduce the image size for now
    # && rm -rf /var/lib/apt/lists/* \
    # && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    # && apt-get clean

COPY ./entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh

ENTRYPOINT [ "/bin/entrypoint.sh" ]
