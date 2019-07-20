#  Copyright (c) 2018 5GTANGO, Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, 5GTANGO, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).

FROM ubuntu:xenial

LABEL maintainer="Manuel Peuster <manuel@peuster.de>"

RUN apt-get update && apt-get install -y \
    net-tools \
    iproute \
    inetutils-ping \
    software-properties-common \
    python3-pip \
    libboost-python-dev \
    libcurl4-openssl-dev

# install latest mosquitto
RUN apt-add-repository -y ppa:mosquitto-dev/mosquitto-ppa
RUN apt-get update
RUN apt-get install -y mosquitto-clients

# install releveant python stuff
RUN pip3 install paho-mqtt
RUN pip3 install prometheus_client

ADD start.sh start.sh
RUN chmod +x start.sh

ADD mqttexporter mqttexporter

# MQTT config
ENV MQTT_BROKER_HOST localhost
ENV MQTT_BROKER_PORT 1883
ENV MQTT_TOPIC +/+/+
ENV PROMETHEUS_EXPORTER_PORT 9089

CMD ./start.sh
