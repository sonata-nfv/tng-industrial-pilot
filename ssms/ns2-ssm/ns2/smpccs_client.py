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
import time
import threading
import grpc
import os
try:  # Docker
    import ns2.smpccs_pb2_grpc as pb2_grpc
    import ns2.smpccs_pb2 as pb2
except:  # tng-sdk-sm
    import smpccs_pb2_grpc as pb2_grpc
    import smpccs_pb2 as pb2


# time to wait until connection retry
TIME_RECONNECT = 3.0


def _state_to_dict(state):
    return {
        "uuid": state.uuid,
        "name": state.name,
        "status": state.status,
        "time_created": state.time_created,
        "time_updated": state.time_updated,
        "changed": state.changed,
        "quarantaine": state.quarantaine
    }


def _update_state_with_dict(state, update):
    state_dict = _state_to_dict(state)
    state_dict.update(update)
    state.uuid = state_dict.get("uuid")
    state.name = state_dict.get("name")
    state.status = state_dict.get("status")
    state.time_created = state_dict.get("time_created")
    state.time_updated = int(time.time())  # set to current time
    state.changed = True  # set update flag
    state.quarantaine = state_dict.get("quarantaine")


class SsmCommandControlClient(threading.Thread):

    def __init__(self, state, connection="localhost:9012", callback=None):
        """
        state: the SSMs state object (type: pb2.SsmState)
        connection: connection string of the remote SMP-CC server.
        callback: function to call when state updates are received.
        """
        super().__init__(daemon=True)
        self.state = state
        self.connection_str = connection
        self.callback_func = callback

    def run(self):
        print("SMP-CC client: started ...")
        while True:  # always retry as long as thread lives
            try:
                print("SMP-CC client: connecting ...")
                with grpc.insecure_channel(self.connection_str) as channel:
                    stub = pb2_grpc.SmpSsmControlStub(channel)
                    # register and wait for state updates
                    print("SMP-CC client: registering state: {}".format(
                        self.state.name))
                    recv_ssm_states = stub.ControlSsm(self.state)
                    # receive state updates from stream (blocking)
                    for new_state in recv_ssm_states:
                        print("SMP-CC client: received SsmState({})".format(
                            _state_to_dict(new_state)))
                        # update the local state
                        _update_state_with_dict(self.state,
                                                _state_to_dict(new_state))
                        print("SMP-CC client: updated local state")
                        if self.callback_func:
                            self.callback_func(new_state)
            except BaseException as ex:
                print("SMP-CC client: Error {}".format(type(ex)))
                print(ex)
                print("SMP-CC client: disconnected")
            print("SMP-CC client: waiting {}s before reconnect ..."
                  .format(TIME_RECONNECT))
            time.sleep(TIME_RECONNECT)


def test_callback(state):
    print("SMP-CC client: quarantaine={}".format(state.quarantaine))


def main():
    # parameters
    name = "ssm01"  # default name
    if len(sys.argv) > 1:
        name = sys.argv[1]

    # get configurations from envs
    con_str = os.getenv("smpcc_grpc_endpoint")
    if con_str is None:
        print("ENV 'smpcc_grpc_endpoint' not specified.")
        print("Exit.")
        exit(1)

    # create state object (this must also be done by SSM)
    state = pb2.SsmState(uuid=name, name=name)
    t = SsmCommandControlClient(
        state,
        connection=con_str,
        callback=test_callback)
    t.start()

    # block (a SSM runs forever)
    while True:
        time.sleep(2)
