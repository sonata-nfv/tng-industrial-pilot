FROM docker.elastic.co/kibana/kibana:6.8.1
MAINTAINER "smpilot@5gtango.eu"
USER root
RUN yum update -y && \
    yum upgrade -y && \
#    yum install -y hostnamectl && \
#    hostnamectl set-hostname kibana --static && \
#    systemctl restart systemd-hostnamed && \
#    sysctl -w kernel.hostname=kibana && \
    yum clean all -y && \
    rm -fr /var/cache/yum

ENV SERVER_NAME="kibana"
ENV XPACK_MONITORING_ENABLED="true"
ENV ELASTICSEARCH_HOSTS="http://elasticsearch"
ENV PATH=$PATH:/usr/share/kibana/bin

USER kibana
WORKDIR /usr/share/kibana/
COPY ./kibana.yml ./config/kibana.yml
COPY ./logging.yml ./config/logging.yml
VOLUME [/usr/share/kibana/data]
EXPOSE 5601/tcp

#ENTRYPOINT ["./bin/../node/bin/node"]
#CMD ["--no-warnings","--max-http-header-size=65536","./bin/../src/cli","--cpu.cgroup.path.override=/","--cpuacct.cgroup.path.override=/","NODE_ENV=production","ELASTIC_CONTAINER=true"]

###
## $ docker build  -t tng-smp-kibana - < Dockerfile
## $ docker run --rm --name kibana -d tng-smp-kibana 
## $ docker exec -it kibana bash
###
