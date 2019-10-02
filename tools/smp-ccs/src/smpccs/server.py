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
from concurrent import futures
import time
import grpc
import smpccs_pb2_grpc as pb2_grpc
import smpccs_pb2 as pb2


UPDATE_INTERVAL = 1.0  # how often to check for updates?


def pprint_state(state, detailed=False):
    print("SsmState({})".format(state.uuid))
    if detailed:
        print("\tname: {}".format(state.uuid))
        print("\tstatus: {}".format(state.status))
        print("\tcreated: {}".format(time.ctime(state.time_created)))
        print("\tupdated: {}".format(time.ctime(state.time_updated)))
        print("\tchanged: {}".format(state.changed))
        print("\tquarantaine: {}".format(state.quarantaine))


class SsmStateStore(object):
    """
    Global state store.
    Stores mapping from UUID to SsmState objects.
    """
    def __init__(self):
        self._store = dict()

    def register(self, state):
        """
        Ads SsmState to store.
        Attention: Simply overwrites existing states.
        """
        # ensure well-formed states:
        if len(state.name) < 1:
            # use a fixed default
            state.name = "default"
        if len(state.uuid) < 1:
            # use name as uuid fallback
            state.uuid = state.name
        if len(state.status) < 1:
            state.status = "undefined"
        # set created and updated timestamps
        state.time_created = int(time.time())
        state.time_updated = int(time.time())
        # TODO locking needed?
        self._store[state.uuid] = state
        print("Registered: ", end="")
        pprint_state(state, True)

    def get(self, uuid):
        return self._store.get(uuid)


# global state store
SS = SsmStateStore()


# implements the RPC methods of SmpSsmControl
class SmpSsmControlServicer(pb2_grpc.SmpSsmControlServicer):

    def PingPong(self, request, context):
        """
        Simple request and reply example.
        """
        print("Received: '{}'".format(request.text))
        reply = pb2.Pong(text="Pong!")
        print("Replying: '{}'".format(reply.text))
        return reply

    def ControlSsm(self, state, context):
        """
        Single Request, streaming reply.
        Keeps open a long-term streaming connection to send
        state updates to the client SSM.
        """
        # 1. register SsmState
        SS.register(state)
        uuid = state.uuid
        created = state.time_created

        # 2. keep connection open and stream out state if its updated
        # loop will stop if SSM registers again!
        while (SS.get(uuid) is not None
               and created == SS.get(uuid).time_created):
            if state.changed:
                yield state  # send out updated state
                state.changed = False
            # FIXME this could be done nicer with a lock, but ok for now
            time.sleep(UPDATE_INTERVAL)
        print("Stopping control for: ", end="")
        pprint_state(state)


def serve():
    print("SMP-CC server starting ...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SmpSsmControlServicer_to_server(
        SmpSsmControlServicer(), server)
    server.add_insecure_port('[::]:9012')
    server.start()
    print("SMP-CC server started: {}".format(server))
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("SMP-CC server stopping ...")
        server.stop(0)
    print("SMP-CC server stopped.")


def main():
    serve()
