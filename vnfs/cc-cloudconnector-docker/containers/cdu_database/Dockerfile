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
    git \
    nginx \
    curl

# install Prometheus from source
# see https://www.techrepublic.com/article/how-to-install-the-prometheus-monitoring-system-on-ubuntu-16-04/
RUN mkdir /etc/prometheus
RUN mkdir /var/lib/prometheus
RUN curl -LO https://github.com/prometheus/prometheus/releases/download/v2.0.0/prometheus-2.0.0.linux-amd64.tar.gz
RUN tar xvf prometheus-2.0.0.linux-amd64.tar.gz
RUN cp prometheus-2.0.0.linux-amd64/prometheus /usr/local/bin/
RUN cp prometheus-2.0.0.linux-amd64/promtool /usr/local/bin/
RUN cp -r prometheus-2.0.0.linux-amd64/consoles /etc/prometheus
RUN cp -r prometheus-2.0.0.linux-amd64/console_libraries /etc/prometheus

ADD prometheus.yml /etc/prometheus/prometheus.yml
ADD start.sh start.sh
RUN chmod +x start.sh

CMD ./start.sh
