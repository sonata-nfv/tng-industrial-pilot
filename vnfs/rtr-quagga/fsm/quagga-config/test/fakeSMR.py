'''
Created on Jun 13, 2017

@author: ubuntu
'''

import time
import logging
import json
import yaml
from sonmanobase import messaging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("son-mano-fakesmr")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)


class fakesmr(object):

    def __init__(self):

        self.name = 'fake-smr'
        self.version = '0.1-dev'
        self.description = 'description'

        LOG.info("Start SMR:...")

        # create and initialize broker connection
        self.manoconn = messaging.ManoBrokerRequestResponseConnection(self.name)

        self.declare_subscriptions()
        LOG.info('End __init__')

    def declare_subscriptions(self):
        """
        Declare topics to which we want to listen and define callback methods.
        """
        self.manoconn.register_async_endpoint(self.on_register_receive, 'specific.manager.registry.ssm.registration')

    def on_register_receive(self,ch, method, properties, payload):

        message = yaml.load(payload)
        LOG.info('message = %s', message)

        response = {
            "status": "registered",
            "specific_manager_type": message['specific_manager_type'],
            "service_name": message['service_name'],
            "function_name": message['function_name'],
            "specific_manager_id": message['specific_manager_id'],
            "version": message['version'],
            "description": message['description'],
            "uuid": '64532',
            "sfuuid": '97456',
            "error": None
        }

        return json.dumps(response)


def main():
    fakesmr()
    while True:
        time.sleep(10)


if __name__ == '__main__':
    main()
