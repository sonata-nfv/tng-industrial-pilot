# Dockerfile with a cusomized configuration for Logstash

FROM logstash:7.3.0
MAINTAINER sm-pilot@5gtango.eu
ENV ELASTICSEARCH_HOSTS=elasticsearch

# CONFIG
#USER logstash
#RUN export ELASTICSEARCH_HOSTS=$( echo $e_vnf3_eu_5gtango_0_4_elastic9200_ip ); echo $ELASTICSEARCH_HOSTS
WORKDIR /usr/share/logstash
COPY logstash.yml ./config/
COPY logstash.conf ./pipeline/
COPY logging.yml ./config/
VOLUME /usr/share/logstash/logs
EXPOSE 5044/tcp 9600/tcp

### USAGE: 
# $ docker build -t tng-smp-logstash .
# $ docker run --rm --name logstash -v /usr/share/logstash/logs:/usr/share/logstash/logs -d tng-smp-logstash
# $ docker exec -it logstash bash
###
