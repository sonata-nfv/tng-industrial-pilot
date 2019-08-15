## STEP 1: GET 'FILEBEAT' FROM OFFICIAL IMAGE REPOSITORY

FROM store/elastic/filebeat:7.3.0
MAINTAINER "smpilot@5gtango.eu"

## STEP 2: CONFIGURE 'FILEBEAT' TO USE 'LOGSTASH'
USER root
ENV LOGSTASH_HOSTS=http://${lh_vnf2_eu_5gtango_0_4_logstash5044_ip:-logstash}:5044
ENV KIBANA_HOSTS=http://${k_vnf4_eu_5gtango_0_4_kibana5601_ip:-kibana}:5601
WORKDIR /usr/share/filebeat
COPY filebeat.yml ./filebeat.yml
RUN chown root:filebeat ./filebeat.yml && \
    chmod go-w ./filebeat.yml
#COPY logging.yml ./
VOLUME /var/log/suricata

## STEP 2: CONFIGURE 'FILEBEAT' TO ENABLE 'SURICATA' MODULE AND 'KIBANA' DASHBOARDS
RUN filebeat modules enable suricata
## Loading dashboards (Kibana must be running and reachable)
   #/usr/share/filebeat/filebeat setup --dashboards && \
   #/usr/share/filebeat/filebeat setup --pipelines --modules suricata && \
   #/usr/share/filebeat/filebeat setup --template


### USAGE:
## $ docker build -t tng-smp-filebeat .
## $ docker run --rm --name filebeat -v /var/log/suricata/:/usr/share/logstash/logs -d tng-smp-filebeat
## $ docker exec --rm  -it filebeat bash
###