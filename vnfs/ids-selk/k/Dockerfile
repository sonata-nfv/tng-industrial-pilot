FROM elastic/kibana:7.4.2
MAINTAINER "smpilot@5gtango.eu"

ENV SERVER_NAME="kibana"
ENV XPACK_MONITORING_ENABLED="true"

USER kibana
WORKDIR /usr/share/kibana
COPY kibana.yml config/kibana.yml
COPY start.sh .
USER root
RUN chmod +x start.sh
USER kibana
EXPOSE 5601/tcp
ENTRYPOINT ./start.sh

#USER root
#RUN chmod +x ./entrypoint.sh
#USER kibana
#ENTRYPOINT ["./entrypoint.sh"]


### USAGE:
## $ docker build -t vnf-ids-kibana .
## $ docker run --rm --name kibana -e "e_vnf3_eu_5gtango_0_8_elastic9200=${e_vnf3_eu_5gtango_0_8_elastic9200_ip}" -d vnf-ids-kibana
## $ docker exec -it kibana bash
###
