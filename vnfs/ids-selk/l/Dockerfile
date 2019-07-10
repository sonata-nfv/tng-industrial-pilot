# Dockerfile with a cusomized configuration for Logstash

FROM docker.elastic.co/logstash/logstash:6.7.1

MAINTAINER sm-pilot@5gtango.eu

# INSTALL 'jq'
USER root
RUN yum clean all && \
    yum update -y && \
    yum install epel-release -y && \
    yum install jq -y && \
    yum clean all && \
    rm -rf /var/cache/yum

# CONFIG
USER logstash
WORKDIR /usr/share/logstash
COPY logstash.yml config/
COPY logstash.conf pipeline/
COPY logging.yml config/
RUN bin/logstash-plugin install logstash-output-exec && bin/logstash-plugin install logstash-input-beats

# RUN DAEMON
COPY docker-entrypoint.sh /usr/local/bin/
RUN chown logstash:root /usr/local/bin/docker-entrypoint.sh && chmod 775 /usr/local/bin/docker-entrypoint.sh
RUN ln -s docker-entrypoint.sh / # backwards compat
ENTRYPOINT ["docker-entrypoint.sh"]
EXPOSE 5044/tcp 9600/tcp

###
# $ docker build  -t tng-smp-ls - < Dockerfile
# $ docker run --rm  -it logstash:6.7.1  bash
###
