# Dockerfile with a cusomized configuration for Logstash

FROM logstash:7.3.0
MAINTAINER sm-pilot@5gtango.eu

# CONFIG
#ARG EU_5GTANGO_E_VNF3_0_4_2A7D7B13_PORT_9200_TCP_ADDR=elasticsearch
#ENV EU_5GTANGO_E_VNF3_0_4_2A7D7B13_PORT_9200_TCP_ADDR=$EU_5GTANGO_E_VNF3_0_4_2A7D7B13_PORT_9200_TCP_ADDR

USER logstash
WORKDIR /usr/share/logstash
COPY logstash.yml ./config/
COPY logstash.conf ./pipeline/
COPY start.sh .
USER root
RUN chown +x start.sh
VOLUME /usr/share/logstash/logs
#VOLUME /usr/share/logstash/data
USER logstash
EXPOSE 5044/tcp 9600/tcp
ENTRYPOINT ["./start.sh"]

### USAGE: 
# $ docker build -t vnf-ids-logstash .
# $ docker run --rm --name logstash -v /var/logs/logstash:/usr/share/logstash/logs -e "e_vnf3_eu_5gtango_0_4_elastic9200_ip=$e_vnf3_eu_5gtango_0_4_elastic9200_ip" -d vnf-ids-logstash
# $ docker exec -it logstash bash
###
