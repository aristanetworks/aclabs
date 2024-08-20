ARG FROM_IMAGE
ARG FROM_VARIANT

FROM ${FROM_IMAGE}:${FROM_VARIANT}

RUN apk update && \
    apk add libteam && \
    apk add open-lldp && \
    apk add sudo && \
    apk add tcpdump && \
    apk add scapy && \
    apk add iperf3

RUN adduser -u 1000 -G wheel -D alpine && \
    echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

COPY ./entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh

USER alpine 

ENTRYPOINT [ "/bin/entrypoint.sh" ]

CMD []
