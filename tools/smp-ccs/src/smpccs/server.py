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


# implements the RPC methods of SmpFsmControl
class SmpFsmControlServicer(pb2_grpc.SmpFsmControlServicer):

    def PingPong(self, request, context):
        """
        Simple request and reply example.
        """
        print("Received: '{}'".format(request.text))
        reply = pb2.Pong(text="Pong!")
        print("Replying: '{}'".format(reply.text))
        return reply

    def ControlFsm(self, request, context):
        """
        Single Request, streaming reply.
        """
        print("ControlFsm received: FsmRegistration({})".format(request.name))
        for i in range(0, 5):
            action = pb2.FsmAction(name="{}".format(i))
            print("Sending: Action({}) to '{}'"
                  .format(action.name, request.name))
            yield action
            # add some waiting time to simulate a real setup
            time.sleep(1.0)


def serve():
    print("SMP-CC server starting ...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SmpFsmControlServicer_to_server(
        SmpFsmControlServicer(), server)
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
