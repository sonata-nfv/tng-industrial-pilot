# Dockerfile with a cusomized configuration for Logstash

FROM ubuntu:16.04

MAINTAINER sm-pilot@5gtango.eu

# [FILEBEAT](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-getting-started.html)

## STEP 1: INSTALL FILEBEAT

# 
RUN apt update -y && \
    apt install -y curl && \
    curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.6.2-amd64.deb && \
    dpkg -i filebeat-6.6.2-amd64.deb && \
    rm -fr filebeat-6.6.2-amd64.deb

## STEP 2: CONFIGURE FILEBEAT

RUN rm -f /etc/filebeat/filebeat.yml
ADD filebeat.yml /etc/filebeat/filebeat.yml
RUN chown root:root /etc/filebeat/filebeat.yml
RUN chmod go-w /etc/filebeat/filebeat.yml

## STEP 3: CONFIGURE FILEBEAT TO USE LOGSTASH
# The recommended index template file for Filebeat is installed by the Filebeat packages. 
# If you accept the default configuration in the filebeat.yml config file, Filebeat loads the template automatically 
## STEP 4:
## STEP 5: Set up the Kibana dashboars

RUN /usr/share/filebeat/bin/filebeat modules enable suricata
RUN /usr/share/filebeat/bin/filebeat setup --dashboards 
RUN /usr/share/filebeat/bin/filebeat setup --pipelines --modules suricata
RUN /usr/share/filebeat/bin/filebeat setup --template
 

#CMD /usr/share/filebeat/bin/filebeat -e -c /etc/filebeat/filebeat.yml -E output.elasticsearch.enabled=false -E output.logstash.enabled=true -E output.logstash.hosts=['localhost:5044']

# Start the Filebeat service 
ENTRYPOINT ["/usr/share/filebeat/bin/filebeat"]
CMD ["-e", "-c","/etc/filebeat/filebeat.yml", "-E","output.elasticsearch.enabled=false","-E","output.logstash.enabled=true","-E","output.logstash.hosts=['localhost:5044']"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
