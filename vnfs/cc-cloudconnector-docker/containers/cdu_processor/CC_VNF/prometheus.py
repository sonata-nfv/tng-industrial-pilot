#  Copyright (c) 2018 5GTANGO, Paderborn University
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
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import time
import random
import os


class CcPrometheusClient(object):

    def __init__(self):
        self.registry = CollectorRegistry()
        self.metrics = dict()
        self.gw_host = os.getenv("PUSH_GATEWAY", "localhost:9091")
        print("CPC: Inititalized Prometheus push client for gateway: {}"
              .format(self.gw_host))

    def _push(self, metric, value):
        """
        Internal push implementation.
        """
        # if we do not have a collector for the given metric yet, we create one
        if metric not in self.metrics:
            m = Gauge(
                metric, "MQTT metric: {}".format(metric),
                registry=self.registry)
            self.metrics[metric] = m
        m = self.metrics[metric]
        print("CPC: Setting metric '{}' to {}".format(metric, value))
        try:
            m.set(float(value))
            print("CPC: Pushing to Prometheus gateway: {}".format(self.gw_host))
            push_to_gateway(self.gw_host, job="cc", registry=self.registry)
        except BaseException as ex:
            print("CPC: Error, couldn't push to Prometheus: {}".format(ex))

    def push_to_db(self, topic, payload):
        """
        Public (safe) push method to be used in CC.
        """
        metric, value = self._topic_to_metric(topic, payload)
        if metric is None or value is None:
            print("CPC: Skipping: {}, {}".format(topic, payload))
            return  # skip
        print("CPC: Try to push ({}, {}) to Prometheus GW ...".format(metric, value), flush=True)
        try:
            self._push(metric, value)
            print("done.")
        except BaseException as ex:
            print("fail. ({})".format(ex))

    def _topic_to_metric(self, topic, payload):
        """
        True to translate topics and payload to Prometheus-safe metric, value.
        If not, print warning and return None, None.
        Return metric, value
        """
        # TODO this method can be improved a lot!
        # - build in fixed translations from strings/states to numbers
        # - build in parsing/translation for hex values
        try:
            metric = str(topic).replace("/", "_")
            metric = metric.replace("@", "")
            metric = metric.strip(" .,-@+")
            metric = metric.lower()
            value = float(payload)
            return metric, value
        except BaseException as ex:
            print("CPC: Couldn't translate to metric, value: {}, {}".format(topic, payload))
            print("CPC: Problem: {}".format(ex)) 
        return None, None


if __name__ == "__main__":
    # simple test and demo how to use CcPrometheusClient
    cpc = CcPrometheusClient()
    while True:
        mlist = ["metric1", "metric2", "metric3", "metric4"]
        # randomly fill the metrics with values
        cpc._push(random.choice(mlist), 100*random.random())
        time.sleep(2)
