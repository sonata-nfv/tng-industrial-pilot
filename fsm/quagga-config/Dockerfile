FROM python:3.5-slim
MAINTAINER SONATA

# configrurations
ENV mongo_host mongo
ENV mongo_port 27017
ENV broker_host amqp://guest:guest@broker:5672/%2F
ENV broker_exchange son-kernel
#
#RUN apt-get clean \
#    && apt-get update \
#    && apt-get install -y wget \
#    && apt-get install -y git build-essential libffi-dev libssl-dev \
#    && wget https://download.docker.com/linux/static/stable/x86_64/docker-17.06.2-ce.tgz \
#    && tar -xzf docker-*-ce.tgz \
#    && cp docker/docker /usr/bin/ \
#    && rm -rf docker-*-ce.tgz docker \
#    && apt-get clean

RUN apt-get update && apt-get -y install python3-pip ssh \
    && apt-get update && pip3 install paramiko && pip3 install ansible \
    && apt-get install -y python3-amqp python3-amqplib \
    && pip3 install IPy

#RUN git clone --recursive https://github.com/sonata-nfv/son-sm.git
#RUN git clone --recursive https://github.com/miguelmesquita/son-security-pilot.git

ADD son-sm/son-mano-framework/son-mano-base /son-mano-base
ADD son-sm/son-sm-template /son-sm-template


#WORKDIR /son-sm/son-mano-framework/son-mano-base
#RUN python setup.py install

#WORKDIR /son-sm/son-sm-template
#RUN python setup.py install

WORKDIR /son-mano-base
Run python setup.py install

WORKDIR /son-sm-template
RUN python setup.py install

#WORKDIR /son-security-pilot/install/roles/docker-squid/files
#COPY ansible/roles/squid/files /etc/squid3

#CMD mkdir /squid-config

WORKDIR /
ADD fsm/squid-config /squid-config

WORKDIR /squid-config
RUN python setup.py develop

#COPY ansible/roles/squid/files/entrypoint.sh /sbin
#RUN chmod 755 /sbin/entrypoint.sh

CMD ["fsm-squid"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
