# Copyright (c) 2019 SONATA-NFV, 5GTANGO and Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
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
# acknowledge the contributions of their colleagues of the 5GTANGO
# partner consortium (www.5gtango.eu).
import logging
from mininet.log import setLogLevel
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint
from emuvim.api.tango import TangoLLCMEndpoint
from emuvim.api.tango.llcm import StaticConfigPlacement


logging.basicConfig(level=logging.DEBUG)
setLogLevel('info')  # set Mininet loglevel
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('5gtango.llcm').setLevel(logging.DEBUG)


def create_topology():
    net = DCNetwork(monitor=False, enable_learning=True)
    # create two data centers
    dc1 = net.addDatacenter("eu-west1")
    dc2 = net.addDatacenter("us-east1")
    dc3 = net.addDatacenter("us-west1")
    dc4 = net.addDatacenter("br-east1")
    dc5 = net.addDatacenter("cn-east1")
    dc6 = net.addDatacenter("au-east1")
    # interconnect data centers
    net.addLink(dc1, dc2, delay="30ms")
    net.addLink(dc2, dc3, delay="5ms")
    net.addLink(dc2, dc4, delay="15ms")
    net.addLink(dc1, dc5, delay="35ms")
    net.addLink(dc5, dc6, delay="10ms")
    # add the command line interface endpoint to the emulated DC (REST API)
    rapi1 = RestApiEndpoint("0.0.0.0", 5001)
    rapi1.connectDCNetwork(net)
    rapi1.connectDatacenter(dc1)
    rapi1.connectDatacenter(dc2)
    rapi1.connectDatacenter(dc3)
    rapi1.connectDatacenter(dc4)
    rapi1.connectDatacenter(dc5)
    rapi1.connectDatacenter(dc6)
    rapi1.start()
    # add the 5GTANGO lightweight life cycle manager (LLCM) to the topology
    # use port 32002 to be able to use tng-cli
    llcm1 = TangoLLCMEndpoint(
        "0.0.0.0", 32002, deploy_sap=False,
        placement_algorithm_obj=StaticConfigPlacement(
            "~/tng-industrial-pilot/emulator-topologies/static_placement.yml"))
    llcm1.connectDatacenter(dc1)
    llcm1.connectDatacenter(dc2)
    llcm1.connectDatacenter(dc3)
    llcm1.connectDatacenter(dc4)
    llcm1.connectDatacenter(dc5)
    llcm1.connectDatacenter(dc6)
    # run the LLCM
    llcm1.start()
    # start the emulation and enter interactive CLI
    net.start()
    net.CLI()
    # when the user types exit in the CLI, we stop the emulator
    net.stop()


def main():
    create_topology()


if __name__ == '__main__':
    main()
