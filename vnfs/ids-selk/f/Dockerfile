## STEP 1: GET 'FILEBEAT' FROM OFFICIAL IMAGE REPOSITORY

FROM store/elastic/filebeat:7.3.0
MAINTAINER "smpilot@5gtango.eu"

## STEP 2: CONFIGURE 'FILEBEAT' TO USE 'LOGSTASH'
ARG LOGSTASH_HOSTS
ARG KIBANA_HOSTS
ENV LOGSTASH_HOSTS=$LOGSTASH_HOSTS
ENV KIBANA_HOSTS=$KIBANA_HOSTS
USER root
WORKDIR /usr/share/filebeat
COPY filebeat.yml ./filebeat.yml
COPY start.sh .
RUN chmod +x start.sh && \
    chown root:filebeat ./filebeat.yml && \
    chmod go-w ./filebeat.yml
#VOLUME /var/log/suricata

## STEP 2: CONFIGURE 'FILEBEAT' TO ENABLE 'SURICATA' MODULE AND 'KIBANA' DASHBOARDS
RUN filebeat modules enable suricata
## Loading dashboards (Kibana must be running and reachable)
   #/usr/share/filebeat/filebeat setup --dashboards && \
   #/usr/share/filebeat/filebeat setup --pipelines --modules suricata && \
   #/usr/share/filebeat/filebeat setup --template
ENTRYPOINT ["start.sh"]


### USAGE:
## $ docker build -t vnf-ids-filebeat .
## $ docker run --rm --name filebeat -v /var/log/suricata/:/usr/share/logstash/logs -d vnf-ids-filebeat
## $ docker run --rm --name my-fb -v /var/log/suricata/:/usr/share/logstash/logs -e "LOGSTASH_HOSTS=http://${lh_vnf2_eu_5gtango_0_4_logstash5044_ip}:5044" -e "KIBANA_HOSTS=http://${k_vnf4_eu_5gtango_0_4_kibana5601_ip}:5601" -d vnf-ids-filebeat
## $ docker exec --rm -it filebeat bash
###
