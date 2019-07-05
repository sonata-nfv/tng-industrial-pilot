#!/bin/bash
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

# Start script to configure Router/NAT using iptables
# 0. change IP if specified (else value from VNFD is used)
[[ -v IFUPLINK_NET ]] && ifconfig uplink $IFUPLINK_NET
# 1. enable ip forwarding
sysctl -w net.ipv4.ip_forward=1
# 2. configure NAT
iptables -t nat -A POSTROUTING -o $IFUPLINK -j MASQUERADE
iptables -A FORWARD -i $IFUPLINK -o $IFLOCAL -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $IFLOCAL -o $IFUPLINK -j ACCEPT

echo "RTR: Configured ip_forward and NAT."
