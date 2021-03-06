# Copyright (c) 2018 5GTANGO, Weidmüller, Paderborn University
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
# Neither the name of the SONATA-NFV, 5GTANGO, Weidmüller, Paderborn University
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
    iptables \
    python3-pip \
    samba-common \
    samba

# install latest mosquitto clients
RUN apt-add-repository -y ppa:mosquitto-dev/mosquitto-ppa
RUN apt-get update
RUN apt-get install -y mosquitto-clients

# install required python libs
RUN pip3 install paho-mqtt

ADD start.sh start.sh
RUN chmod +x start.sh
ADD mqtt_generator.sh mqtt_generator.sh
RUN chmod +x mqtt_generator.sh

# Samba configuration
ADD smb.conf /etc/samba/smb.conf

# MDC application
ADD MDC_VNF MDC_VNF

# folder for euromap communication
ADD em63_share em63_share
# allow everybody to write to our share (enables guest access over samba)
RUN chmod 777 em63_share

# network config
ENV IFLOCAL data
ENV NETNS1 30.0.1.0/24
ENV GATEWAY 30.0.3.3

# MQTT config
ENV MQTT_BROKER_HOST 30.0.1.1
ENV MQTT_BROKER_PORT 1883
# name of the connected machine (used as first part of MQTT topic)
ENV MACHINE_NAME WIMMS

# MDC configs
# (dont change, its also hardcoded in smb.conf)
ENV MDC_EM63_SHARE_FOLDER /em63_share

CMD ./start.sh

# Samba 139, 445 TCP and 137, 138 UDP
EXPOSE 139
EXPOSE 445
EXPOSE 137/udp
EXPOSE 138/udp
