#  Copyright (c) 2018 5GTANGO, Weidmüller, Paderborn University
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
    smbclient \
    cifs-utils \
	autofs

ENV LC_ALL C.UTF-8

# install required python libs
RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy autofs configuration
ADD auto.master /etc/autofs/auto.master
ADD auto.em63 /etc/autofs/auto.em63

# digital twin tool
ADD IMMS_APP IMMS_APP
# folder for euromap communication
ADD em63_share em63_share

ADD start.sh start.sh
RUN chmod +x start.sh
ADD stop.sh stop.sh
RUN chmod +x stop.sh

# configuration
ENV DT_WEB_LISTEN 0.0.0.0
ENV DT_WEB_PORT 15001
ENV DT_EM63_SHARE /em63_share
# mdc in emulator: 30.0.1.2 local testing: 172.17.0.2
ENV DT_EM63_SHARE_HOST 30.0.1.2
ENV OPCUA_HOST localhost
ENV OPCUA_PORT 4840

CMD ./start.sh

# DT's webinterface port
EXPOSE 15001
