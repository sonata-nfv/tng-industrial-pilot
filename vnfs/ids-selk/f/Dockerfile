## STEP 1: GET 'FILEBEAT' FROM OFFICIAL IMAGE REPOSITORY

FROM store/elastic/filebeat:7.3.0
MAINTAINER "smpilot@5gtango.eu"

## STEP 2: CONFIGURE 'FILEBEAT' TO USE 'LOGSTASH'
USER root
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

# add start.sh
ADD start.sh start.sh
RUN chmod +x start.sh && \
    chown root:filebeat ./start.sh
ENTRYPOINT ["./start.sh"]


## USAGE:
## $ docker build -t tng-smp-filebeat .
## $ docker run --rm --name filebeat -v /var/log/suricata/:/usr/share/logstash/logs -d tng-smp-filebeat
## $ docker exec --rm  -it filebeat bash
##
