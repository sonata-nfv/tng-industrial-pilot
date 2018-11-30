FROM ubuntu:16.04
MAINTAINER 'AR, arocha@ptinovacao.pt'
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:oisf/suricata-stable && \
    apt-get update && \
    apt-get install -y suricata
#CMD ["cat", "/etc/os-release"]
