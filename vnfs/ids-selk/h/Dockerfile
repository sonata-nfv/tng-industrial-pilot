FROM ubuntu:latest
MAINTAINER Miguel Mesquita "mesquita@alticelabs.com"
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev build-essential
ENV container_name=logstash
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["httptangosrv.py"]

##
## docker build -t tng-smp-flask .
## docker run -t flask -d tng-smp-flask
## docker exec -it flask bash
##