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
import time
from smbase.smbase import smbase


logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("fsm-mdc")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)

ENV_MQTT_HOST_NORMAL = "MQTT_BROKER_HOST"
ENV_MQTT_HOST_QUARANTINE = "QUARANTINE_MQTT_BROKER_HOST"


class mdcFSM(smbase):

    def __init__(self, connect_to_broker=True):
        """
        :param specific_manager_type: specifies the type of specific manager
        that could be either fsm or ssm.
        :param service_name: the name of the service that this specific manager
        belongs to.
        :param function_name: the name of the function that this specific
        manager belongs to, will be null in SSM case
        :param specific_manager_name: the actual name of specific manager
        (e.g., scaling, placement)
        :param id_number: the specific manager id number which is used to
        distinguish between multiple SSM/FSM that are created for the same
        objective (e.g., scaling with algorithm 1 and 2)
        :param version: version
        :param description: description
        """

        self.sm_id = "tng-fsm-industry-pilot-mdc-vnf1"
        self.sm_version = "0.1"

        super(self.__class__, self).__init__(sm_id=self.sm_id,
                                             sm_version=self.sm_version,
                                             connect_to_broker=connect_to_broker)

    def on_registration_ok(self):

        # The fsm registration was successful
        LOG.debug("Received registration ok event.")

        # send the status to the SMR
        status = 'Subscribed, waiting for alert message'
        message = {'name': self.sm_id,
                   'status': status}
        self.manoconn.publish(topic='specific.manager.registry.ssm.status',
                              message=yaml.dump(message))

        # Subscribing to the topics that the fsm needs to listen on
        topic = "generic.fsm." + str(self.sfuuid)
        self.manoconn.subscribe(self.message_received, topic)
        LOG.info("Subscribed to " + topic + " topic.")

    def message_received(self, ch, method, props, payload):
        """
        This method handles received messages
        """

        # Decode the content of the message
        request = yaml.load(payload)

        # Don't trigger on non-request messages
        if "fsm_type" not in request.keys():
            LOG.info("Received a non-request message, ignoring...")
            return

        # Create the response
        response = None

        # the 'fsm_type' field in the content indicates for which type of
        # fsm this message is intended.
        if str(request["fsm_type"]) == "start":
            LOG.info("Start event received: " + str(request["content"]))
            response = self.start_event(request["content"])

        if str(request["fsm_type"]) == "stop":
            LOG.info("Stop event received: " + str(request["content"]))
            response = self.stop_event(request["content"])

        if str(request["fsm_type"]) == "configure":
            LOG.info("Config event received: " + str(request["content"]))
            response = self.configure_event(request["content"])

        # If a response message was generated, send it back to the FLM
        LOG.info("Response to request generated:" + str(response))
        topic = "generic.fsm." + str(self.sfuuid)
        corr_id = props.correlation_id
        self.manoconn.notify(topic,
                             yaml.dump(response),
                             correlation_id=corr_id)
        return

    def start_event(self, content):
        """
        This method handles a start event.
        """

        # Dummy content
        LOG.info("MDC FSM: start event triggered")
        response = {'status': 'completed'}
        return response

    def stop_event(self, content):
        """
        This method handles a stop event.
        """

        # Dummy content
        LOG.info("MDC FSM: stop event triggered")
        response = {'status': 'completed'}
        return response

    def configure_event(self, content):
        """
        This method handles a configure event. The configure event changes the configuration
        of the MDC to connect it to a different NS1 ("Shadow Copy").
        """
        LOG.info("MDC FSM: Starting configuration event")
        
        # get hostname of the quarantine NS1 from the NSR. Note: Only possible if set as instantiation param, when starting the NS (not preconfigured env)!
        # example content: http://logs.sonata-nfv.eu/messages/graylog_65/fbe87433-f568-11e9-a4e4-0242ac130004
        cdu_id = None
        normal_ns1_host = None
        quarantine_ns1_host = None
        error_msg = ""
        # ENVs are given per CDU. Search for CDU01 (MDC)
        for cdu in content['generic_envs']:
            id = cdu['cdu_id']
            if id.startswith('cdu01'):
                # this is the MDC CDU
                cdu_id = id
                normal_ns1_host = cdu['envs'].get(ENV_MQTT_HOST_NORMAL)
                quarantine_ns1_host = cdu['envs'].get(ENV_MQTT_HOST_QUARANTINE)
                break  # stop (we don't care about the other CDUs)

        if normal_ns1_host is None:
            error_msg += "MDC FSM: '{}' not found in envs //".format(ENV_MQTT_HOST_NORMAL)

        if quarantine_ns1_host is None:
            error_msg += "MDC FSM: '{}' not found in envs //".format(ENV_MQTT_HOST_QUARANTINE)
                
        if cdu_id is None:
            error_msg += "MDC FSM: MDC cdu01 ID not found //"
            LOG.error(error_msg)

        if len(error_msg) > 0:
            # Error happened. Print all errs.
            LOG.error("MDC FSM: Error! {}".format(error_msg))
        else:
            error_msg = "None"  # not sure if None is really expected by the MANO framework

        LOG.debug("MDC FSM status: normal_ns1_host={}".format(normal_ns1_host))
        LOG.debug("MDC FSM status: quarantine_ns1_host={}".format(quarantine_ns1_host))

        # reconfigure MDC: overwrite existing MQTT broker host
        response = {
            'status': 'COMPLETED',
            'envs': [{
                'cdu_id': cdu_id,
                'envs': {
                    ENV_MQTT_HOST_NORMAL: quarantine_ns1_host,
                    ENV_MQTT_HOST_QUARANTINE: quarantine_ns1_host
                    }
                }],
            'error': error_msg
            } 
        LOG.info("MDC FSM: Configuration event completed")
        LOG.debug("MDC FSM response: {}".format(response))
        return response


def main():
    LOG.info("MDC FSM: main()")
    mdcFSM()


if __name__ == '__main__':
    main()
