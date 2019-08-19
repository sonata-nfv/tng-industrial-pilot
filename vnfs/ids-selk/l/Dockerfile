# Dockerfile with a cusomized configuration for Logstash

FROM logstash:7.3.0
MAINTAINER sm-pilot@5gtango.eu

# CONFIG
ARG e_vnf3_eu_5gtango_0_4_elastic9200_ip
ENV ELASTICSEARCH_HOSTS=http://${e_vnf3_eu_5gtango_0_4_elastic9200_ip:-elasticsearch}:9200
WORKDIR /usr/share/logstash
COPY logstash.yml ./config/
COPY logstash.conf ./pipeline/
VOLUME /usr/share/logstash/logs
VOLUME /usr/share/logstash/data
EXPOSE 5044/tcp 9600/tcp
CMD ["bin/logstash"]

### USAGE: 
# $ docker build -t vnf-ids-logstash .
# $ docker run --rm --name logstash -v /var/logs/logstash:/usr/share/logstash/logs -e "ELASTICSEARCH_HOSTS=$e_vnf3_eu_5gtango_0_4_elastic9200_ip" -d vnf-ids-logstash
# $ docker exec -it logstash bash
###
