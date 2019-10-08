## STEP 1: GET 'FILEBEAT' FROM OFFICIAL IMAGE REPOSITORY

FROM elastic/filebeat:7.3.2
MAINTAINER "smpilot@5gtango.eu"

## STEP 2: CONFIGURE 'FILEBEAT' TO USE 'LOGSTASH'
ARG LOGSTASH_HOSTS
ARG KIBANA_HOST
ENV LOGSTASH_HOSTS=$LOGSTASH_HOSTS
ENV KIBANA_HOST=$KIBANA_HOST
WORKDIR /usr/share/filebeat
COPY filebeat.yml .
COPY start.sh .
USER root
#VOLUME /var/log/suricata
VOLUME /usr/share/filebeat/data
RUN usermod -aG filebeat root && \
    chmod +x start.sh && \
    chown root:filebeat filebeat.yml start.sh && \
    chmod go-w filebeat.yml
USER filebeat
WORKDIR /usr/share/filebeat

## STEP 2: CONFIGURE 'FILEBEAT' TO ENABLE 'SURICATA' MODULE AND 'KIBANA' DASHBOARDS
RUN filebeat modules enable suricata
## Loading dashboards (Kibana must be running and reachable)
#    filebeat setup --pipelines
#    filebeat setup --index-management
#    filebeat setup --dashboards
ENTRYPOINT ./start.sh

### USAGE:
## $ docker build -t vnf-ids-filebeat .
## $ docker run --rm --name filebeat -v /var/log/suricata/:/usr/share/logstash/logs -d vnf-ids-filebeat
## $ docker run --rm --name my-fb -v /var/log/suricata/:/usr/share/logstash/logs -e "LOGSTASH_HOSTS=http://${lh_vnf2_eu_5gtango_0_8_logstash5044_ip}:5044" -e "KIBANA_HOSTS=http://${k_vnf4_eu_5gtango_0_8_kibana5601_ip}:5601" -d vnf-ids-filebeat
## $ docker exec --rm -it filebeat bash
###
