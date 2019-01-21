FROM ubuntu:16.04
MAINTAINER 'AR, arocha@ptinovacao.pt'
RUN apt-get clean -y && \
    apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y libpcre3 libpcre3-dbg libpcre3-dev build-essential libpcap-dev \
            libnet1-dev libyaml-0-2 libyaml-dev pkg-config zlib1g zlib1g-dev    \
            libcap-ng-dev libcap-ng0 make libmagic-dev libjansson-dev            \
            libnss3-dev libgeoip-dev liblua5.1-dev libhiredis-dev libevent-dev && \
    apt-get install libnetfilter-queue-dev libnetfilter-queue1  \
            libnetfilter-log-dev libnetfilter-log1 \
            libnfnetlink-dev libnfnetlink0 &&       \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:oisf/suricata-stable && \
    apt-get update -y && \
    apt-get install -y suricata

#CMD ["cat", "/etc/os-release"]
