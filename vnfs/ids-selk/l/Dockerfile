# Dockerfile with a cusomized configuration for Logstash

FROM logstash:7.3.2
MAINTAINER sm-pilot@5gtango.eu

# CONFIG
ARG VERSION=0.6
ARG EU_5GTANGO_E_VNF3_0_6_PORT_9200_TCP_ADDR
ARG SMB_CLIENT_NAME
ARG SMB_USER_NAME
ARG ELASTICSEARCH_HOSTS

ENV EU_5GTANGO_E_VNF3_0_6_PORT_9200_TCP_ADDR=$EU_5GTANGO_E_VNF3_0_6_PORT_9200_TCP_ADDR
ENV SMB_CLIENT_NAME=$SMB_CLIENT_NAME
ENV SMB_USER_NAME=$SMB_USER_NAME
ENV ELASTICSEARCH_HOSTS=$ELASTICSEARCH_HOSTS

USER logstash
WORKDIR /usr/share/logstash
COPY logstash.yml config/logstash.yml
COPY logstash.conf pipeline/logstash.conf
COPY start.sh .
USER root
RUN chmod +x start.sh
VOLUME /usr/share/logstash/logs
#VOLUME /usr/share/logstash/data
USER logstash
EXPOSE 5044/tcp 9600/tcp
ENTRYPOINT ["./start.sh"]
CMD [VERSION]

### USAGE: 
# $ docker build -t vnf-ids-logstash .
# $ docker run --rm --name logstash -v /var/logs/logstash:/usr/share/logstash/logs -e "e_vnf3_eu_5gtango_0_6_elastic9200_ip=$e_vnf3_eu_5gtango_0_6_elastic9200_ip" -d vnf-ids-logstash
# $ docker exec -it logstash bash
###
