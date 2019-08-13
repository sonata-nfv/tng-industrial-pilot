## STEP 1: GET 'FILEBEAT' FROM OFFICIAL IMAGE REPOSITORY

FROM store/elastic/filebeat:7.3.0
MAINTAINER "smpilot@5gtango.eu"

## STEP 2: CONFIGURE 'FILEBEAT' TO USE 'LOGSTASH'
#USER filebeat
ARG lh_vnf2_eu_5gtango_0_4_logstash5044_ip
ARG e_vnf3_eu_5gtango_0_4_elastic9200_ip
ENV LOGSTASH_HOSTS=${lh_vnf2_eu_5gtango_0_4_logstash5044_ip:-logstash}
ENV ELASTICSEARCH_HOSTS=${e_vnf3_eu_5gtango_0_4_elastic9200_ip:-elasticsearch}
WORKDIR /usr/share/filebeat
COPY filebeat.yml ./
COPY logging.yml ./
VOLUME /var/log/suricata

## STEP 2: CONFIGURE 'FILEBEAT' TO ENABLE 'SURICATA' MODULE AND 'KIBANA' DASHBOARDS
RUN /usr/share/filebeat/filebeat modules enable suricata
## Loading dashboards (Kibana must be running and reachable)
   #/usr/share/filebeat/filebeat setup --dashboards && \
   #/usr/share/filebeat/filebeat setup --pipelines --modules suricata && \
   #/usr/share/filebeat/filebeat setup --template


## USAGE:
## $ docker build -t tng-smp-filebeat .
## $ docker run --rm --name filebeat -v /var/log/suricata/:/usr/share/logstash/logs -d tng-smp-filebeat
## $ docker exec --rm  -it filebeat bash
##
