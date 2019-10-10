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
from flask import Flask, Blueprint
from flask_restplus import Resource, Api, Namespace
from flask_restplus import inputs
from werkzeug.contrib.fixers import ProxyFix


UPDATE_INTERVAL = 1.0  # how often to check for updates?


# Basic setup of REST server for API
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint('api', __name__, url_prefix="/api")
api_v1 = Namespace("v1", description="SMP-CCS API v1")
api = Api(blueprint,
          version="0.1",
          title='SMP-CCS API',
          description="5GTANGO SMP-CCS REST API " +
          "to control the industry pilot SSM.")
app.register_blueprint(blueprint)
api.add_namespace(api_v1)


def serve_rest_api(service_address="0.0.0.0",
                   service_port=9011,
                   debug=True):
    app.run(host=service_address,
            port=int(service_port),
            debug=debug,
            # do not use the reloder: to avoid restarts and stat loss
            use_reloader=False)


ssmstate_put_parser = api_v1.parser()
ssmstate_put_parser.add_argument("uuid",
                                 type=str,
                                 required=True,
                                 help="Service Inst. UUID")
ssmstate_put_parser.add_argument("quarantaine",
                                 type=inputs.boolean,
                                 required=False,
                                 help="Updated quarantaine status")


@api_v1.route("/ssmstatus")
class SsmStateEndpoint(Resource):

    @api_v1.response(200, "OK")
    def get(self):
        return app.store.get_dict()

    @api_v1.expect(ssmstate_put_parser)
    @api_v1.response(200, "OK")
    @api_v1.response(404, "Service UUID not found")
    def put(self):
        args = ssmstate_put_parser.parse_args()
        print(args)
        return "OK"


class SsmStateStore(object):
    """
    Global state store.
    Stores mapping from UUID to SsmState objects.
    """
    def __init__(self):
        print("Created: {}".format(self))
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

    def get_dict(self):
        """
        Returns all entries as a standard dict.
        uuid -> state
        """
        r = dict()
        for k, v in self._store.items():
            r[k] = _state_to_dict(v)
        return r

    def get(self, uuid):
        return self._store.get(uuid)


def pprint_state(state, detailed=False):
    print("SsmState({})".format(state.uuid))
    if detailed:
        for k, v in _state_to_dict(state).items():
            print("\t{}: {}".format(k, v))


def _state_to_dict(state):
    return {
        "uuid": state.uuid,
        "status": state.status,
        "created": state.time_created,
        "updated": state.time_updated,
        "changed": state.changed,
        "quarantaine": state.quarantaine
    }


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
        self.store.register(state)
        uuid = state.uuid
        created = state.time_created

        # 2. keep connection open and stream out state if its updated
        # loop will stop if SSM registers again!
        while (self.store.get(uuid) is not None
               and created == self.store.get(uuid).time_created):
            if state.changed:
                yield state  # send out updated state
                state.changed = False
            # FIXME this could be done nicer with a lock, but ok for now
            time.sleep(UPDATE_INTERVAL)
        print("Stopping control for: ", end="")
        pprint_state(state)


def serve():
    print("SMP-CC server starting ...")
    store = SsmStateStore()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = SmpSsmControlServicer()
    servicer.store = store
    pb2_grpc.add_SmpSsmControlServicer_to_server(
        servicer, server)
    server.add_insecure_port('[::]:9012')
    server.start()
    print("SMP-CC server started: {}".format(server))
    try:
        # start the REST API server (blocks)
        app.store = store
        serve_rest_api()
    except KeyboardInterrupt:
        print("SMP-CC server stopping ...")
        server.stop(0)
    print("SMP-CC server stopped.")


def main():
    serve()
