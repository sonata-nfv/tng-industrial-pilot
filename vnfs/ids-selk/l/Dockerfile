# Dockerfile with a cusomized configuration for Logstash

FROM docker.elastic.co/logstash/logstash:6.8.1

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
COPY logstash.yml ./config/
COPY logstash.conf ./pipeline/
COPY logging.yml ./config/
VOLUME /usr/share/logstash/logs

# RUN DAEMON
EXPOSE 5044/tcp 9600/tcp
#RUN bin/logstash-plugin install logstash-output-exec && bin/logstash-plugin install logstash-input-beats
#COPY docker-entrypoint.sh /usr/local/bin/
#RUN chown logstash:root /usr/local/bin/docker-entrypoint.sh && chmod 775 /usr/local/bin/docker-entrypoint.sh
#RUN ln -s docker-entrypoint.sh / # backwards compat
#ENTRYPOINT ["docker-entrypoint.sh"]

###
# $ docker build -t tng-smp-logstash - < Dockerfile
# $ docker run --rm --name logstash -v /usr/share/logstash/logs:/usr/share/logstash/logs -d tng-smp-logstash
# $ docker exec -it logstash bash
###
