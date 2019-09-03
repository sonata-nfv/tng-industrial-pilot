FROM elastic/kibana:7.3.0
MAINTAINER "smpilot@5gtango.eu"

#ARG EU_5GTANGO_E_VNF3_0_4_2A7D7B13_PORT_9200_TCP_ADDR=elasticsearch
#ENV EU_5GTANGO_E_VNF3_0_4_2A7D7B13_PORT_9200_TCP_ADDR=$EU_5GTANGO_E_VNF3_0_4_2A7D7B13_PORT_9200_TCP_ADDR
#ENV ELASTICSEARCH_HOSTS=$EU_5GTANGO_E_VNF3_0_4_2A7D7B13_PORT_9200_TCP_ADDR
ENV SERVER_NAME="kibana"
ENV XPACK_MONITORING_ENABLED="true"

USER kibana
WORKDIR /usr/share/kibana
COPY kibana.yml config/kibana.yml
COPY start.sh .
RUN chmod +x start.sh
EXPOSE 5601/tcp
ENTRYPOINT ["./start.sh"]

#USER root
#RUN chmod +x ./entrypoint.sh
#USER kibana
#ENTRYPOINT ["./entrypoint.sh"]


### USAGE:
## $ docker build -t vnf-ids-kibana .
## $ docker run --rm --name kibana -e "e_vnf3_eu_5gtango_0_4_elastic9200=${e_vnf3_eu_5gtango_0_4_elastic9200_ip}" -d vnf-ids-kibana
## $ docker exec -it kibana bash
###
