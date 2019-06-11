# Dockerfile with a cusomized configuration for Logstash

FROM docker.elastic.co/logstash/logstash:6.7.1

MAINTAINER sm-pilot@5gtango.eu

# INSTALL 'jq'
USER root
RUN yum update -y && \
    yum install epel-release -y && \
    yum install jq -y && \
    yum clean all
#COPY logstash-entry.sh /usr/local/bin/logstash-entry.sh
#RUN chown logstash:root /usr/local/bin/logstash-entry.sh && chmod 775 /usr/local/bin/logstash-entry.sh

# CONFIG
USER logstash
EXPOSE 5044/tcp
EXPOSE 9600/tcp
WORKDIR /usr/share/logstash
RUN bin/logstash-plugin install logstash-output-exec && bin/logstash-plugin install logstash-input-beats

# RUN DAEMON
#ENTRYPOINT ["/usr/local/bin/logstash-entry.sh"]
ENTRYPOINT ["bin/logstash"]
#CMD ["logstash-plugin", "install", "logstash-output-exec"]
