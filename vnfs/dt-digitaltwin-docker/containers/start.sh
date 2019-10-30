#!/bin/bash
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

set -e

echo "DT: Wait for MDC ... (3 seconds)"
sleep 3  # ok, lets give the MDC some time to start Samba ... (ugly but works)

echo "DT: Mount em63_share from MDC ..."
#mount -t cifs -o guest //$DT_EM63_SHARE_HOST/guest $DT_EM63_SHARE

# auto fs: set MDC address in configs, then start autofs
sed "s/EM63_HOST/$DT_EM63_SHARE_HOST/" /etc/autofs/auto.master
sed "s/EM63_HOST/$DT_EM63_SHARE_HOST/" /etc/autofs/auto.em63
service autofs restart
sleep 2


echo "DT: Starting DigitalTwin generator ..."
cd IMMS_APP
python3 IMMS_APP.py --autostart
cd /
