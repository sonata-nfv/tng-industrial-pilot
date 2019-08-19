FROM elastic/kibana:7.3.0
MAINTAINER "smpilot@5gtango.eu"

ARG e_vnf3_eu_5gtango_0_4_elastic9200_ip
ENV e_vnf3_eu_5gtango_0_4_elastic9200_ip=${e_vnf3_eu_5gtango_0_4_elastic9200_ip:-elasticsearch}
ENV ELASTICSEARCH_HOSTS=http://${e_vnf3_eu_5gtango_0_4_elastic9200_ip}:9200
ENV SERVER_NAME="kibana"
ENV XPACK_MONITORING_ENABLED="true"
ENV PATH=$PATH:/usr/share/kibana/bin

VOLUME [/usr/share/kibana/data]
EXPOSE 5601/tcp

WORKDIR /usr/share/kibana
COPY kibana.yml config/kibana.yml
CMD ["bin/kibana"]

### USAGE:
## $ docker build -t vnf-ids-kibana .
## $ docker run --rm --name kibana -e "e_vnf3_eu_5gtango_0_4_elastic9200=${e_vnf3_eu_5gtango_0_4_elastic9200_ip}" -d vnf-ids-kibana
## $ docker exec -it kibana bash
###
