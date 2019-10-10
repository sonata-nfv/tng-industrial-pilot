# Dockerfile with a cusomized configuration for Logstash

FROM logstash:7.3.2
MAINTAINER sm-pilot@5gtango.eu

# CONFIG
ARG SMB_CLIENT_NAME=pre-int-sp-ath
ARG SMB_USER_NAME=tango

ENV SMB_CLIENT_NAME=$SMB_CLIENT_NAME
ENV SMB_USER_NAME=$SMB_USER_NAME

USER logstash
WORKDIR /usr/share/logstash
COPY logstash.yml config/logstash.yml
COPY logstash.conf pipeline/logstash.conf
COPY start.sh .
USER root
RUN chmod +x start.sh && \
    chown logstash:root start.sh
VOLUME /usr/share/logstash/logs
#VOLUME /usr/share/logstash/data
USER logstash
EXPOSE 5044/tcp 9600/tcp

ENTRYPOINT ./start.sh

### USAGE: 
# $ docker build -t vnf-ids-logstash .
# $ docker run --rm --name logstash -v /var/logs/logstash:/usr/share/logstash/logs -e "e_vnf3_eu_5gtango_0_8_elastic9200_ip=$e_vnf3_eu_5gtango_0_8_elastic9200_ip" -d vnf-ids-logstash
# $ docker exec -it logstash bash
###
