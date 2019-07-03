# Dockerfile with a cusomized configuration for Logstash

FROM docker.elastic.co/logstash/logstash:6.7.1

MAINTAINER sm-pilot@5gtango.eu

# INSTALL 'jq'
USER root
RUN yum update -y && \
    yum install epel-release -y && \
    yum install jq -y && \
    yum clean all && \
    rm -rf /var/cache/yum
#COPY logstash-entry.sh /usr/local/bin/logstash-entry.sh
#RUN chown logstash:root /usr/local/bin/logstash-entry.sh && chmod 775 /usr/local/bin/logstash-entry.sh

# CONFIG
USER logstash
COPY ./logstash.yml /usr/share/logstash/config/logstash.yml
COPY ./logging.yml /usr/share/logstash/config/logging.yml
WORKDIR /usr/share/logstash
RUN bin/logstash-plugin install logstash-output-exec && bin/logstash-plugin install logstash-input-beats
EXPOSE 5044/tcp 9600/tcp

# RUN DAEMON
ENTRYPOINT ["bin/logstash"]
