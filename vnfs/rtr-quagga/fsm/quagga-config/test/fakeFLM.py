'''
Created on Jun 13, 2017

@author: ubuntu
'''

import logging
import json
import yaml
import time
from sonmanobase import messaging

LOG = logging.getLogger("son-mano-fakeflm")
LOG.setLevel(logging.DEBUG)
logging.getLogger("son-mano-base:messaging").setLevel(logging.INFO)


class fakeflm(object):
    def __init__(self):

        self.name = 'fake-flm'
        self.version = '0.1-dev'
        self.description = 'description'

        LOG.info("Start sending VNFR:...")

        # create and initialize broker connection
        self.manoconn = messaging.ManoBrokerRequestResponseConnection(self.name)

        self.manoconn.subscribe(self._on_publish,'son.configuration')

        self.end = False

        self.publish_nsd()

        self.run()

    def run(self):

        # go into infinity loop

        while self.end == False:
            time.sleep(1)

    def publish_nsd(self):

        LOG.info("Sending VNFR")
        vnfr = open('vnfr.yml', 'r')
        message = {'VNFR':yaml.load(vnfr)}
        self.manoconn.publish('son.configuration', json.dumps(message))
        vnfr.close()
        self.end = True

    def _on_publish(self, ch, method, props, response):

        LOG.info("_on_publish")
        if props.app_id != self.name:
            response = json.loads(response)
            if type(response) == dict:
                try:
                    print(response)
                except BaseException as error:
                    print(error)


def main():
    fakeflm()


if __name__ == '__main__':
    main()
