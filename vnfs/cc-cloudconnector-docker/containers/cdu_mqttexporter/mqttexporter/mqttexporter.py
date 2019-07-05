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
import os
from paho.mqtt import client as mqttc
from prometheus_client import Gauge
from prometheus_client import start_http_server as start_export_http_server


class MqttExporter(object):

    def __init__(self, mqtt_host, mqtt_port, mqtt_topic, exporter_port):
        self.mqtt_host = mqtt_host
        self.mqtt_port = int(mqtt_port)
        self.mqtt_topic = mqtt_topic
        self.exporter_port = int(exporter_port)
        self._metric_registry = dict()  # dict of Prometheus Metrics
        print("MQE: Initialized MqttExporter for broker '{}:{}' exporting on {}"
              .format(self.mqtt_host, self.mqtt_port, self.exporter_port))

    def _start_prometheus_exporter(self):
        """
        Starts a simple server to export the prometheus metrics.
        """
        start_export_http_server(self.exporter_port)

    def _update_metric(self, metric, label, value, is_numeric):
        """
        Wraps Prometheus client and updates values of Prometheus metrics.
        Everthing is stored as Gauge.
        Numeric values are stored directly, other (strings) are stored
        as labels and a counter value is increased for the given label.
        """
        # ensure singelton instance of Metric objects
        if metric not in self._metric_registry:
            self._metric_registry[metric] = Gauge(
                metric, "Metric {}".format(metric), ["machine", "message"])
        # update metric
        if is_numeric:  # directly set the numeric value
            self._metric_registry[metric].labels(machine=label, message="numeric").set(value)
            print("MQE:\tPrometheus set numeric metric '{}' to {}".format(metric, value))
        else:  # use the mesaage as label and increment message counter
            self._metric_registry[metric].labels(machine=label, message=value).inc()
            print("MQE:\tPrometheus inc. labeld metric '{}' message={}".format(metric, value))

    def _topic_to_metric_label(self, topic):
        """
        Prometheus has restrictions on metric names.
        """
        try:
            prts = str(topic).split("/")
            label = prts[0]
            metric = "_".join(prts[1:])
            #metric = str(topic).replace("/", "_")
            metric = metric.replace("@", "")
            metric = metric.strip(" .,-@+")
            return metric.lower(), label
        except BaseException as ex:
            print("MQE: Can't translate topic: {}".format(topic))
            print("MQE: - Exception: {}".format(ex)) 
        return None, None

    def _clean_payload(self, topic):
        """
        Prometheus has restrictions on payloads.
        """
        try:
            metric = str(topic).replace("/", "_")
            metric = metric.replace("@", "")
            metric = metric.strip(" .,-@+")
            return metric.lower()
        except BaseException as ex:
            print("MQE: Can't translate topic: {}".format(topic))
            print("MQE: - Exception: {}".format(ex)) 
        return None

    def _payload_to_value(self, payload):
        """
        Prometheus supports only numeric values.
        If a string is given is_numeric=False for
        workaround with labels.
        Order of cast tries:
        - float
        - hex w. prefix
        - hex w/o. prefix
        Returns: value, is_numeric
        """
        # floats
        try:
            return float(payload), True
        except BaseException as ex:
            pass
        # hex (try1)
        try:
            return float(int(payload.lower(), 16)), True
        except BaseException as ex:
            pass
        # hex (try2)
        try:
            return float(int("0x{}".format(payload.lower()), 16)), True
        except BaseException as ex:
            pass
        return str(self._clean_payload(payload)), False

    def _get_on_message_callback(self):
        """
        Closure creating the on_message callback
        """
        def on_message(client, userdata, message):
            if message is None:
                return
            msg_topic = str(message.topic)
            msg_payload = str(message.payload.decode("utf-8"))
            print("MQE: Received MQTT message on '{}': {}"
                  .format(msg_topic, msg_payload.rstrip()), flush=True)
            try:
                m, l = self._topic_to_metric_label(msg_topic)
                # update prometheus metric
                self._update_metric(m, l,
                    *self._payload_to_value(msg_payload))  # expand tuple to value, is numeric
            except BaseException as ex:
                print("MQE: Prometheus error: {}".format(ex))
        # return on_message function 
        return on_message

    def _mqtt_subscribe(self):
        self.mqtt_client = mqttc.Client("MqttPrometheusExporter")
        self.mqtt_client.on_message = self._get_on_message_callback()
        print("MQE: Connecting to MQTT broker: {}:{}".format(self.mqtt_host, self.mqtt_port))
        self.mqtt_client.connect(self.mqtt_host, port=self.mqtt_port)
        print("MQE: Subscribing to MQTT topic {}".format(self.mqtt_topic))
        self.mqtt_client.subscribe(self.mqtt_topic)
        #self.mqtt_client.loop_start()  # non blocking
        self.mqtt_client.loop_forever()  # blocking

    def start(self):
        # initialize Prometheus exporter
        self._start_prometheus_exporter()
        # subscribe to mqtt
        self._mqtt_subscribe()

def main():
    me = MqttExporter(
        os.getenv("MQTT_BROKER_HOST", "127.0.0.1"),
        os.getenv("MQTT_BROKER_PORT", 1883),
        os.getenv("MQTT_TOPIC", "WIMMS/EM63/#"),
        os.getenv("PROMETHEUS_EXPORTER_PORT", 9089))
    me.start()

if __name__ == "__main__":
    main()
