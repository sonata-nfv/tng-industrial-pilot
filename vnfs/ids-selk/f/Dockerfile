## STEP 1: GET FILEBEAT FROM OFFICIAL IMAGE REPOSITORY

FROM elastic/filebeat:6.8.1
MAINTAINER "smpilot@5gtango.eu"
USER root
RUN yum update -y && \
    yum upgrade -y && \
    yum clean all -y && \
    rm -fr /var/cache/yum
    #hostnamectl set-hostname filebeat

## STEP 2: CONFIGURE FILEBEAT TO USE LOGSTASH
USER filebeat
WORKDIR /usr/share/filebeat
COPY filebeat.yml ./
COPY logging.yml ./

## STEP 2: CONFIGURE FILEBEAT TO ENABLE suricata MODULE AND kibana DASHBOARDS
RUN /usr/share/filebeat/filebeat modules enable suricata
## Loading dashboards (Kibana must be running and reachable)
   #/usr/share/filebeat/filebeat setup --dashboards && \
   #/usr/share/filebeat/filebeat setup --pipelines --modules suricata && \
   #/usr/share/filebeat/filebeat setup --template

# START filebeat LOG SHIPPER
#ENTRYPOINT ["/usr/share/filebeat/filebeat"]
#CMD ["-e", "-c","/etc/filebeat/filebeat.yml", "-E","output.elasticsearch.enabled=false","-E","output.logstash.enabled=true","-E","o utput.logstash.hosts=['logstash:5044']"]

###
# $ docker build  -t tng-smp-filebeat - < Dockerfile
# $ docker run --rm --name filebeat -d tng-smp-filebeat
# $ docker exec --rm  -it filebeat  bash
###