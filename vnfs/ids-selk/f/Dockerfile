# Dockerfile with a cusomized configuration for Logstash

FROM ubuntu:16.04

MAINTAINER sm-pilot@5gtango.eu

# [FILEBEAT](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-getting-started.html)

## STEP 1: INSTALL FILEBEAT

# 
RUN apt update -y && \
    apt install -y curl && \
    curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.6.0-amd64.deb && \
    dpkg -i filebeat-6.6.0-amd64.deb && \
    rm -fr ./filebeat-6.6.0-amd64.deb

## STEP 2: CONFIGURE FILEBEAT

RUN rm -f /usr/share/filebeat/filebeat.yml
ADD ./filebeat.yml /usr/share/filebeat/filebeat.yml
RUN chown root /usr/share/filebeat/filebeat.yml
RUN chmod 0644 /usr/share/filebeat/filebeat.yml

## STEP 3: CONFIGURE FILEBEAT TO USE LOGSTASH
# The recommended index template file for Filebeat is installed by the Filebeat packages. 
# If you accept the default configuration in the filebeat.yml config file, Filebeat loads the template automatically 

RUN filebeat modules enable logstash
RUN filebeat modules enable suricata

#RUN filebeat setup --template -E output.logstash.enabled=false -E 'output.elasticsearch.hosts=["localhost:9200"]'

## STEP 4:

## STEP 5: Set up the Kibana dashboars
 
CMD filebeat setup && filebeat -e
#    -E output.logstash.enabled=false \
#    -E output.elasticsearch.hosts=['localhost:9200'] \
#    -E setup.kibana.host=localhost:5601

# Start the Filebeat service 
#CMD service filebeat start

