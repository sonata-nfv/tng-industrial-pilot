## STEP 1: GET 'FILEBEAT' FROM OFFICIAL IMAGE REPOSITORY

FROM store/elastic/filebeat:7.3.0
MAINTAINER "smpilot@5gtango.eu"
#USER root
#RUN yum update -y && \
#    yum upgrade -y && \
#    yum clean all -y && \
#    rm -fr /var/cache/yum
    #hostnamectl set-hostname filebeat
#RUN export LOGSTASH_HOSTS=$( echo $lh_vnf2_eu_5gtango_0_4_logstash5044_ip ); echo $LOGSTASH_HOSTS
#RUN export ELASTICSEARCH_HOSTS=$( echo $e_vnf3_eu_5gtango_0_4_elastic9200_ip ); echo $ELASTICSEARCH_HOSTS

## STEP 2: CONFIGURE 'FILEBEAT' TO USE 'LOGSTASH'
#USER filebeat
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

RUN export LOGSTASH_HOSTS=$( echo $lh_vnf2_eu_5gtango_0_4_logstash5044_ip ); echo $LOGSTASH_HOSTS
RUN export ELASTICSEARCH_HOSTS=$( echo $e_vnf3_eu_5gtango_0_4_elastic9200_ip ); echo $ELASTICSEARCH_HOSTS

## USAGE:
## $ docker build -t tng-smp-filebeat .
## $ docker run --rm --name filebeat -v /var/log/suricata/:/usr/share/logstash/logs -d tng-smp-filebeat
## $ docker exec --rm  -it filebeat bash
##
