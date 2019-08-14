# Dockerfile with a cusomized configuration for Logstash

FROM logstash:7.3.0
MAINTAINER sm-pilot@5gtango.eu

# CONFIG
WORKDIR /usr/share/logstash
COPY logstash.yml ./config/
COPY logstash.conf ./pipeline/
#COPY logging.yml ./config/
VOLUME /usr/share/logstash/logs
EXPOSE 5044/tcp 9600/tcp

# add start.sh
USER root
ADD start.sh start.sh
RUN chmod +x start.sh && \
    chown logstash:root ./start.sh
USER logstash
ENTRYPOINT ["./start.sh"]


### USAGE: 
# $ docker build -t tng-smp-logstash .
# $ docker run --rm --name logstash -v /usr/share/logstash/logs:/usr/share/logstash/logs -d tng-smp-logstash
# $ docker exec -it logstash bash
###
