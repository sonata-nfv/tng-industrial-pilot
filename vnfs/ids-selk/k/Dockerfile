FROM kibana:7.3.0
MAINTAINER "smpilot@5gtango.eu"
#USER root
#RUN yum update -y && \
#    yum upgrade -y && \
#    yum install -y hostnamectl && \
#    hostnamectl set-hostname kibana --static && \
#    systemctl restart systemd-hostnamed && \
#    sysctl -w kernel.hostname=kibana && \
#    yum clean all -y && \
#    rm -fr /var/cache/yum

#ARG e_vnf4_eu_5gtango_0_4_kibana5601_ip
#ARG e_vnf3_eu_5gtango_0_4_elastic9200_ip
# docker build --build-arg some_variable_name=a_value

#USER kibana
ENV SERVER_NAME="kibana"
ENV XPACK_MONITORING_ENABLED="true"
ENV ELASTICSEARCH_HOSTS=elasticseach
ENV PATH=$PATH:/usr/share/kibana/bin
WORKDIR /usr/share/kibana/
COPY ./kibana.yml ./config/kibana.yml
COPY ./logging.yml ./config/logging.yml
VOLUME [/usr/share/kibana/data]
EXPOSE 5601/tcp

RUN export ELASTICSEARCH_HOSTS=$( echo $e_vnf3_eu_5gtango_0_4_elastic9200_ip ); echo $ELASTICSEARCH_HOSTS

###
## $ docker build  -t tng-smp-kibana - < Dockerfile
## $ docker run --rm --name kibana -d tng-smp-kibana 
## $ docker exec -it kibana bash
###
