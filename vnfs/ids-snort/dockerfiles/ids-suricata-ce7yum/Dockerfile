FROM centos:7.5.1804
MAINTAINER 'AR, arocha@ptinovacao.pt'
RUN yum clean all && \
    yum update -y && \
    #yum upgrade -y && \
    yum install -y epel-release && \
    yum update && \
    yum install -y suricata
#CMD ["cat", "/etc/os-release"]
