FROM docker.elastic.co/kibana/kibana:6.7.1
MAINTAINER "smpilot@5gtango.eu"
RUN yum update -y
ENV SERVER_NAME="kibana"
ENV XPACK_MONITORING_ENABLED="true"
ENV ELASTICSEARCH_HOSTS="http://elasticsearch"
ENV PATH=$PATH:/usr/share/kibana/bin
USER kibana
WORKDIR /usr/share/kibana/
COPY ./kibana.yml ./config/kibana.yml
COPY ./logging.yml ./config/logging.yml
VOLUME [/usr/share/kibana/data]
EXPOSE 5601/tcp

#ENTRYPOINT ["kibana"]
#CMD ["-d","-v"]
