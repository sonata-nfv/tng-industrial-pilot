# Dockerfile with a cusomized configuration for Logstash

FROM docker.elastic.co/logstash/logstash:6.6.0

MAINTAINER sm-pilot@5gtango.eu

RUN rm -f /usr/share/logstash/pipeline/logstash.conf
RUN rm -f /usr/share/logstash/config/logstash.yml

ADD ./suricata-beats.conf /usr/share/logstash/pipeline/suricata-beats.conf
ADD ./suricata-beats.conf /usr/share/logstash/config/suricata-beats.conf
ADD ./logstash.yml /usr/share/logstash/config/logstash.yml
