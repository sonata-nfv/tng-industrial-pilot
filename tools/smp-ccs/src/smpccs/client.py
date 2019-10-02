#  Copyright (c) 2015 SONATA-NFV, 5GTANGO, Paderborn University
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

import sys
import grpc
import smpccs_pb2_grpc as pb2_grpc
import smpccs_pb2 as pb2


def main():
    print("SMP-CC test client connecting ...")
    with grpc.insecure_channel("localhost:9012") as channel:
        stub = pb2_grpc.SmpSsmControlStub(channel)
        # first test to send a simple PingPong
        ping = pb2.Ping(text="Ping!")
        print("Sending: '{}'".format(ping.text))
        pong = stub.PingPong(ping)
        print("Received: '{}'".format(pong.text))
        # second: connect, register and wait for streamed actions
        name = "ssm01"  # default name
        if len(sys.argv) > 1:
            name = sys.argv[1]
        fsm_state = pb2.SsmState(name=name)
        print("Registering FSM: SsmState({})".format(fsm_state.name))
        new_fsm_states = stub.ControlSsm(fsm_state)
        # receive actions (blocking) from stream
        for state in new_fsm_states:
            print("Received SsmState({})".format(state.name))

    print("SMP-CC test client stopped.")
