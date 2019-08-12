# Dockerfile with a cusomized configuration for Logstash

FROM docker.elastic.co/logstash/logstash:7.3.0

MAINTAINER sm-pilot@5gtango.eu

# INSTALL 'jq'
USER root
RUN yum clean all && \
    yum update -y && \
    yum install epel-release -y && \
    yum install jq -y && \
    yum clean all && \
    rm -rf /var/cache/yum

# CONFIG
USER logstash
WORKDIR /usr/share/logstash
COPY logstash.yml ./config/
COPY logstash.conf ./pipeline/
COPY logging.yml ./config/
VOLUME /usr/share/logstash/logs

# RUN DAEMON
EXPOSE 5044/tcp 9600/tcp
RUN export ELASTICSEARCH_HOSTS=$( echo $e_vnf3_eu_5gtango_0_4_elastic9200_ip ); echo $ELASTICSEARCH_HOSTS

### USAGE: 
# $ docker build -t tng-smp-logstash .
# $ docker run --rm --name logstash -v /usr/share/logstash/logs:/usr/share/logstash/logs -d tng-smp-logstash
# $ docker exec -it logstash bash
###
