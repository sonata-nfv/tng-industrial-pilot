FROM elastic/kibana:7.3.0
MAINTAINER "smpilot@5gtango.eu"

ARG e_vnf3_eu_5gtango_0_4_elastic9200_ip=elasticsearch
ENV e_vnf3_eu_5gtango_0_4_elastic9200_ip=$e_vnf3_eu_5gtango_0_4_elastic9200_ip
#ENV ELASTICSEARCH_HOSTS=$e_vnf3_eu_5gtango_0_4_elastic9200_ip
ENV SERVER_NAME="kibana"
ENV XPACK_MONITORING_ENABLED="true"

WORKDIR /usr/share/kibana
COPY kibana.yml config/kibana.yml
EXPOSE 5601/tcp
ENTRYPOINT bin/kibana -e http://${e_vnf3_eu_5gtango_0_4_elastic9200_ip}:9200

#USER root
#RUN chmod +x ./entrypoint.sh
#USER kibana
#ENTRYPOINT ["./entrypoint.sh"]


### USAGE:
## $ docker build -t vnf-ids-kibana .
## $ docker run --rm --name kibana -e "e_vnf3_eu_5gtango_0_4_elastic9200=${e_vnf3_eu_5gtango_0_4_elastic9200_ip}" -d vnf-ids-kibana
## $ docker exec -it kibana bash
###
