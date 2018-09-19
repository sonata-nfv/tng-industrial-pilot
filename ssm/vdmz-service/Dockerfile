# Copyright (c) 2015 SONATA-NFV
# ALL RIGHTS RESERVED.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).

FROM python:3.6-slim
MAINTAINER SONATA

# configrurations
ENV mongo_host mongo
ENV mongo_port 27017
ENV broker_host amqp://guest:guest@broker:5672/%2F
ENV broker_exchange son-kernel

RUN apt-get clean \
    && apt-get update \
    && apt-get install -y build-essential iputils-ping netcat

ADD son-sm/son-mano-framework/son-mano-base /son-mano-base
ADD son-sm/son-sm-template /son-sm-template

WORKDIR /son-mano-base
Run python setup.py install

WORKDIR /son-sm-template
RUN python setup.py install

WORKDIR /
ADD ssm/vdmz-service /vdmz_service

WORKDIR /vdmz_service
RUN python setup.py develop

CMD ["vdmz_service"]

