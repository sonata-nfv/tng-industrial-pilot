FROM ubuntu:latest
MAINTAINER Miguel Mesquita "mesquita@alticelabs.com"
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev build-essential
ENV container_name=logstash
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
#VOLUME /usr/share/logstash/logs
ENTRYPOINT ["python3"]
CMD ["httptangosrv.py"]

##
## docker build -t vnf-ids-http .
## docker run -t http -v /usr/share/logstash/logs:/var/log/logstash -d vnf-ids-http
## docker exec -it http bash
##
