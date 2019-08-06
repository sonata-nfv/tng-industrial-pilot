#  Copyright (c) 2015 SONATA-NFV, 5GTANGO, UBIWHERE, Paderborn University
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
# Neither the name of the SONATA-NFV, 5GTANGO, UBIWHERE, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).


FROM ubuntu:xenial
LABEL maintainer="Stefan Schneider <stefan.schneider@upb.de>"


# install python and grafana
USER root
RUN apt-get update -y
RUN apt-get install -y --fix-missing apt-utils python3 python3-pip software-properties-common curl apt-transport-https wget adduser libfontconfig1
RUN add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
RUN curl https://packages.grafana.com/gpg.key | apt-key add -
RUN apt-get update -y
RUN apt-get install -y grafana net-tools iproute iputils-ping

# copy script and install requirements
COPY reconfigure_grafana.py reconfigure_grafana.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy config files for provisioning and pre-configuring the data source and dashboard
COPY datasource.yml /etc/grafana/provisioning/datasources/datasource.yml
COPY dashboard_provider.yml /etc/grafana/provisioning/dashboards/dashboard_provider.yml
COPY dashboard.json /var/lib/grafana/dashboards/dashboard.json

# set Grafana admin password to "tango" (to avoid initial prompt for password change)
ENV GF_SECURITY_ADMIN_PASSWORD tango

# env vars for connection to CC Prometheus DB
ENV eu.5gtango_smpilot-cc_0.1_prometheus_ip 192.168.99.100
ENV eu.5gtango_smpilot-cc_0.1_prometheus_port 9090

# add start.sh
ADD start.sh start.sh
RUN chmod +x start.sh

CMD ./start.sh
