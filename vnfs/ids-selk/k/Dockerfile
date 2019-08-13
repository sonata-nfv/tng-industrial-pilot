FROM kibana:7.3.0
MAINTAINER "smpilot@5gtango.eu"

USER root
WORKDIR /
RUN echo $e_vnf3_eu_5gtango_0_4_elastic9200_ip && \
    echo "elasticsearch ${e_vnf3_eu_5gtango_0_4_elastic9200_ip}.default.pod.cluster.local" > /etc/host.aliases && \
    echo "export HOSTALIASES=/etc/host.aliases" >> /etc/bashrc
ENV HOSTALIASES=/etc/host.aliases

USER kibana
ENV ELASTICSEARCH_HOSTS=http://elasticsearch:9200
ENV SERVER_NAME="kibana"
ENV XPACK_MONITORING_ENABLED="true"
ENV PATH=$PATH:/usr/share/kibana/bin
WORKDIR /usr/share/kibana/

COPY ./kibana.yml ./config/kibana.yml
COPY ./logging.yml ./config/logging.yml
VOLUME [/usr/share/kibana/data]
EXPOSE 5601/tcp

###
## $ docker build  -t tng-smp-kibana - < Dockerfile
## $ docker run --rm --name kibana -d tng-smp-kibana 
## $ docker exec -it kibana bash
###
