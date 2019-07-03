FROM docker.elastic.co/elasticsearch/elasticsearch:6.7.1
MAINTAINER "smpilot@5gtango.eu"
#RUN yum update -y
ENV ES_JAVA_OPTS="-Xms1g -Xmx1g"
ENV ES_HEAP_SIZE="2g"
ENV bootstrap.memory_lock="true"
ENV discovery.type="single-node"
ENV PATH=$PATH:/usr/share/elasticsearch/bin
USER elasticsearch
COPY ./elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
COPY ./logging.yml /usr/share/elasticsearch/config/logging.yml
WORKDIR /usr/share/elasticsearch
VOLUME [/usr/share/elasticsearch/data]
EXPOSE 9200/tcp 9300/tcp

#ENTRYPOINT ["elasticsearch"]
#CMD ["-d","-v"]
