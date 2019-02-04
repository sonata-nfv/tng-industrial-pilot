# Dockerfile with a cusomized configuration for Logstash

FROM docker.elastic.co/logstash/logstash:6.6.0

MAINTAINER sm-pilot@5gtango.eu

RUN rm -fr /usr/share/logstash/logstash.conf
ADD ./beats2elastic.conf /usr/share/logstash/beats2elastic.conf
ADD ./beats2elastic.conf /usr/share/logstash/config/beats2elastic.conf

RUN rm -fr /usr/share/logstash/logstash.yml
ADD ./logstash.yml /usr/share/logstash/logstash.yml
ADD ./logstash.yml /usr/share/logstash/config/logstash.yml

