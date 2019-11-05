"""
Copyright (c) 2015 SONATA-NFV, 2017 5GTANGO
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV, 5GTANGO
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).

This work has been performed in the framework of the 5GTANGO project,
funded by the European Commission under Grant number 761493 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the 5GTANGO
partner consortium (www.5gtango.eu).
"""

import logging
import yaml
import os
import time
import tnglib
from smbase.smbase import smbase
try:  # Docker
    from ns2.smpccs_client import SsmCommandControlClient
    from ns2.smpccs_pb2 import SsmState
    INIT_DELAY = 1  # only wait a small amount of time
except:  # tmg-sdk-sm
    from smpccs_client import SsmCommandControlClient
    from smpccs_pb2 import SsmState
    INIT_DELAY = 5  # wait longer for debugging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("ssm-ns2")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)


class ns2SSM(smbase):

    def __init__(self, connect_to_broker=True):
        """
        :param connect_to_to_broker: connect manager to broker or not
        """

        self.sm_id = "tng-ssm-industry-pilot-ns2"
        self.sm_version = "0.1"

        # local state/info initialized during initial configuration event
        # local copy of service info (configuration event content)
        self._service_info = None
        # state of the service (e.g. quarantaine yes/no)
        self._service_state = None

        super(self.__class__, self).__init__(sm_id=self.sm_id,
                                             sm_version=self.sm_version,
                                             connect_to_broker=connect_to_broker)

    def subscribe(self):

        LOG.info("Subscribing...")

        # Subscribing to the topics that the ssm needs to listen on
        topic = "generic.ssm." + str(self.sfuuid)
        self.manoconn.subscribe(self.message_received, topic)
        LOG.info("Subscribed to " + topic + " topic.")

    def on_registration_ok(self):

        # The ssm registration was successful
        LOG.debug("Received registration ok event.")

        # send the status to the SMR
        status = 'Subscribed, waiting for alert message'
        message = {'name': self.sm_id,
                   'status': status}
        self.manoconn.publish(topic='specific.manager.registry.ssm.status',
                              message=yaml.dump(message))

    def message_received(self, ch, method, props, payload):
        """
        This method handles received messages
        """

        # Decode the content of the message
        request = yaml.load(payload)

        # Don't trigger on non-request messages
        if "ssm_type" not in request.keys():
            LOG.info("Received a non-request message, ignoring...")
            return

        # Create the response
        response = None

        # the 'ssm_type' field in the content indicates for which type of
        # ssm this message is intended.
        if str(request["ssm_type"]) == "placement":
            LOG.info("Placement event received: " + str(request["content"]))
            response = self.placement_event(request["content"])

        if str(request["ssm_type"]) == "task":
            LOG.info("Task event received: " + str(request))
            response = self.task_event(request)

        if str(request["ssm_type"]) == "configure":
            LOG.info("Config event received: " + str(request))
            response = self.configure_event(request)

        if str(request["ssm_type"]) == "state":
            LOG.info("State event received: " + str(request["content"]))
            response = self.state_event(request["content"])

        # If a response message was generated, send it back to the FLM
        LOG.info("Response to request generated:" + str(response))
        topic = "generic.ssm." + str(self.sfuuid)
        corr_id = props.correlation_id
        self.manoconn.notify(topic,
                             yaml.dump(response),
                             correlation_id=corr_id)
        return

    def placement_event(self, content):
        """
        This method handles a placement event.
        """

        # Dummy content
        response = {'status': 'COMPLETED'}
        return response

    def task_event(self, content):
        """
        This method handles a task event.
        """

        # Update the received schedule
        schedule = content['schedule']

        schedule.insert(11, 'configure_ssm')

        response = {'schedule': schedule, 'status': 'COMPLETED'}

        LOG.info("task request responded to: " + str(response))

        return response

    def configure_event(self, content):
        """
        This method handles a configure event.
        It calls either an initial configuration or a
        reconfiguration of the MDC.
        """
        if content['workflow'] == 'instantiation':
            LOG.info("NS2 SSM: configure/instantiation event triggered")
            return self._configure_event_instantiation(content)
        else:
            LOG.info("NS2 SSM: configure/reconfiguration event triggered")
            return self._configure_event_reconfiguration(content)

    def _get_service_instance_uuid(self):
        try:
            return self._service_info['service']['id']
        except BaseException as ex:
            LOG.error("NS2 SSM: Coudn't fetch instance UUID: {}"
                      .format(ex))
            return None

    def _get_service_name(self):
        try:
            vendor = self._service_info['service']['nsd']['vendor']
            name = self._service_info['service']['nsd']['name']
            version = self._service_info['service']['nsd']['version']
            return "{}.{}.{}".format(vendor, name, version)
        except BaseException as ex:
            LOG.error("NS2 SSM: Coudn't fetch service name: {}"
                      .format(ex))
            return None

    def _configure_event_instantiation(self, content):
        """
        Configure event called upon instantiaten of the service.
        It is used to collect basic information of the service instance
        and establishes the connection to the external control server (SMP-CC).
        """
        response = {'status': 'COMPLETED', 'vnf': []}
        # store local copy of service information for later use
        self._service_info = content.copy()
        LOG.debug("NS2 SSM: Stored service instance information: {}"
                  .format(self._service_info))

        # initialize local service state
        suuid = self._get_service_instance_uuid()
        sname = self._get_service_name()
        if suuid is not None and sname is not None:
            self._service_state = SsmState(uuid=suuid, name=sname)

        # get address of remote SMP-CC server
        con_str = os.getenv("smpcc_grpc_endpoint")
        if con_str is None:
            LOG.error("NS2 SSM: Could not find 'smpcc_grpc_endpoint'")

        # initialize SMP-CC client and connect to remote control server
        if con_str is not None and self._service_state is not None:
            smpccc = SsmCommandControlClient(
                self._service_state,
                connection=con_str,
                callback=None)
            smpccc.start()  # runs in dedicated daemon thread

        # Give the client some time start
        # TODO this is an ugly hack! better build a lock-based mechanism
        LOG.info("NS2 SSM: Waiting for SMP-CC client to start ({}s)"
                 .format(INIT_DELAY))
        time.sleep(INIT_DELAY)

        # TODO: Implement callback upon remote state change! and call: self._print_state()
        # TODO: Trigger reconfig event using the content from self._service_info

        # done
        LOG.info("NS2 SSM: configure/instantiation event completed")
        LOG.debug("NS2 SSM: configure/instantiation event response: {}"
                  .format(response))
        return response

    def _configure_event_reconfiguration(self, content):
        """
        Configure event called upon reconfiguration (e.g. called by the policy
        manager or the SMP-CC server from the FMP).
        It indicates an intrusion and should trigger a reconfiguration event.
        The reconfiguration event is forwarded to the MDC FSM.
        """
        response = {'status': 'COMPLETED', 'vnf': []}
        # get IDs of all VNF instances
        for vnf in content['functions']:
            # create the response
            vnf_name = vnf['vnfr']['name']
            vnf_dict = {
                'id': vnf['vnfr']['id'],
                'name': vnf_name,
                'configure': {'trigger': False}
            }
            # trigger reconfig only for MDC VNF
            if vnf_name == 'msf-vnf1':
                vnf_dict['configure']['trigger'] = True
                vnf_dict['configure']['payload'] = {'message': 'IDS Alert 1'}
            # build the response
            response['vnf'].append(vnf_dict)
        # try to update internal state
        self._set_quarantaine(True)
        # TODO (optional): trigger a callback function to update state at SMP-CCS
        # done
        LOG.info("NS2 SSM: configure/reconfiguration event completed")
        LOG.debug("NS2 SSM: configure/reconfiguration event response: {}"
                  .format(response))
        return response

    def _set_quarantaine(self, value):
        # FIXME: add locks for thread safety
        if self._service_state is None:
            LOG.error("NS2 SSM: Cannot set state. State store is None.")
            return
        LOG.info("NS2 SSM: setting quarantaine state")
        self._service_state.quarantaine = value
        self._print_state()

    def _print_state(self):
        if self._service_state is None:
            LOG.error("NS2 SSM: Cannot print state. State store is None.")
            return
        LOG.info("NS2 SSM: quarantaine state is: {}"
                 .format(self._service_state.quarantaine))

    def state_event(self, content):
        """
        This method handles a state event.
        """

        # Dummy content
        response = {'status': 'COMPLETED'}
        response['content'] = 'the new state'
        return response


def main():
    ns2SSM()


if __name__ == '__main__':
    main()
