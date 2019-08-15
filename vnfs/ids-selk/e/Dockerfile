FROM elasticsearch:7.3.0
MAINTAINER "smpilot@5gtango.eu"

USER elasticsearch
ENV ES_JAVA_OPTS="-Xms1g -Xmx1g"
ENV ES_HEAP_SIZE="2g"
ENV bootstrap.memory_lock="true"
ENV discovery.type="single-node"
ENV PATH=$PATH:/usr/share/elasticsearch/bin
WORKDIR /usr/share/elasticsearch
COPY elasticsearch.yml ./config/
#COPY logging.yml ./config/
VOLUME [/usr/share/elasticsearch/data]
EXPOSE 9200/tcp 9300/tcp

## USAGE: 
## $ docker build -t tng-smp-elasticsearch .
## $ docker run --rm --name elasticsearch -d tng-smp-elasticsearch
## $ docker exec -it elasticsearch bash
###