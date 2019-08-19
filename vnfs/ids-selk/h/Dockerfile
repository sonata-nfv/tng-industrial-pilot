FROM ubuntu:latest
MAINTAINER Miguel Mesquita "mesquita@alticelabs.com"
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev build-essential
ENV container_name=logstash
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
#VOLUME /usr/share/logstash/logs
ENTRYPOINT ["python"]
CMD ["httptangosrv.py"]

##
## docker build -t vnf-ids-http .
## docker run -t http -v /usr/share/logstash/logs:/var/log/logstash -d vnf-ids-http
## docker exec -it http bash
##
