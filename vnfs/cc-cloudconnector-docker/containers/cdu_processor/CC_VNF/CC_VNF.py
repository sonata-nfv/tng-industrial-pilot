#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 5GTANGO, Weidmüller, Paderborn University
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
# Neither the name of the SONATA-NFV, 5GTANGO, Weidmüller, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).
"""
    File name: CC_VNF.py
    Description: Cloud Connector Azure
    Version: 2019-02-28
    Python Version 3.6.7
    Editor: Spyder (indentation characters: 4 spaces)
    Maintainer: Marcel Müller <Marcel.Mueller@weidmueller.com>
    Copyright: 2018, Marcel Müller, Weidmüller Group, Detmold, Germany
"""

import time
import os
import sys
import json
import paho.mqtt.client as paho
from paho.mqtt import client as azure_mqtt
import ssl
from SASGenerator import SASGenerator as sas


def cc_config(config_file):
    print("---------------------------------------------")
    global deviceKey, iot_hub_name, device_id, sas_token
    # Import json file for SAS token, if available
    if os.path.exists(config_file):
        try:
            with open(config_file) as file:
                keyData = json.load(file)[0]  # Simplified workaround with [0]
            sas_token = keyData["sas_token"]  # SAS token of device
            if sas_token == '':
                print("No SAS token available.")
            else:
                print("SAS token is available: " + str(sas_token))
            iot_hub_name = keyData["hub_name"]  # Name of IoT Hub
            if iot_hub_name == '':
                print("IoT Hub name is missing. Check JSON file.")
                return 1
            else:
                print("IoT Hub name found: " + str(iot_hub_name))
            device_id = keyData["device_id"]  # Name of device to connect to
            if device_id == '':
                print("Device name is missing. Check JSON file.")
                return 1
            else:
                print("Name of device found: " + str(device_id))
            # Try to generate SAS token if entry is empty
            if sas_token == '':
                device_key = keyData["primary_key"]  # primary key of device
                if device_key == '':
                    print("Can not generate SAS token.")
                    print("Primary key is missing. Check JSON file.\n")
                    return 1
                else:
                    print("Primary key found: " + str(device_key))
                if iot_hub_name != '' and device_id != '' and device_key != '':
                    print("Try to generate SAS token.")
                    uri = iot_hub_name + ".azure-devices.net/devices/" \
                        + device_id
                    print("URL to device: " + str(uri))
                    # Time in seconds the SAS token should expire.
                    expireTime = 3600
                    print("Expire time: " + str(expireTime))
                    # Generate sas_token for cloud connection
                    sas_token = sas.generate_sas_token(uri,
                                                       device_key,
                                                       policy_name=None,
                                                       expiry=expireTime)
                    if sas_token != '':
                        print("SAS token generated: " + str(sas_token) + "\n")
                else:
                    print("Can not generate SAS token. \n")
                    return 1
            return 0
        except OSError:
            print("Exception detected while opening file: ", config_file)
            print("\n")
            return 1
    else:
        print("Configuration file not found: ", config_file)
        print("\n")
        return 1


# MQTT functions for Azure IoT Hub
def on_connectA(client, userdata, flags, rc):
    print("Device connected with result code: " + str(rc))
    print("---------------------------------------------")


def on_disconnectA(client, userdata, rc):
    print("Device disconnected with result code: " + str(rc))
    print("---------------------------------------------")


def on_publishA(client, userdata, mid):
    print("Device sent message to cloud.")
    print("---------------------------------------------\n")


# MQTT function
def on_message(client, userdata, message):
    global payload3, payload4
    payload_str = str(message.payload.decode("utf-8"))
    topic_str = str(message.topic)
    # construct a message for cloud backend
    msgstr = build_message(topic_str, payload_str)
    # transform data
    if topic_str == topicstr3:
        payload3 = float(payload_str)
    if topic_str == topicstr4:
        payload4 = float(payload_str)
    # send message to cloud backend
    if msgstr != 0:
        send_message(msgstr)


def build_message(topic, payload):
    global listetopic, listepayload
    print("Received message from MQTT broker: ")
    print("Topic: %s Payload: %s" % (topic, payload))
    if topic in listetopic:
        msgstr = "{"
        for index in range(len(listetopic)):
            msgstr += "\"%s\": %s" % (str(listetopic[index]),
                                      str(listepayload[index]))
            if index < len(listetopic)-1:
                msgstr += ","
        msgstr += "}"
        del listetopic
        del listepayload
        listetopic = []
        listepayload = []
        listetopic.append(topic)
        listepayload.append(payload)
        return msgstr
        # return msgdict
    else:
        listetopic.append(topic)
        listepayload.append(payload)
        return 0


def send_message(msg):
    global payload3, payload4
    # print("RAW message: %s" % msg)

    # Case A: Em63 parameters
#    messageA = IoTHubMessage(msg)
#    print("Sending message: %s" % messageA.get_string() )
#    clientA.send_event_async(messageA, send_confirmation_callback, None)

    # Case B: dummy values
#    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#    sin=2
#    data = [{"Date": date, "Sinus": sin}]
#    messageA = IoTHubMessage(json.dumps(data))
#    print("Sending message: %s \n" % messageA.get_string() )
#    clientA.send_event_async(messageA, send_confirmation_callback, None)

    # Case C: Em63 parameters
    # use a dictionary instead of a string
    # topicstr1 = "WIMMS/EM63/DATE"
    # topicstr2 = "WIMMS/EM63/@ActSimPara2"

    MSG_TXT = "{\"%s\": %.2f,\"%s\": %.2f}"
    # payload3=12
    # payload4=2*payload3
    msg_txt_formatted = MSG_TXT % (topicstr3, payload3, topicstr4, payload4)
    messageA = msg_txt_formatted  # IoTHubMessage(msg_txt_formatted)
    print("---------------------------------------------")
    print("Send messages to cloud.")
    print("Sending message: %s" % messageA)
    # Push to Azure IoT Hub
    clientA.loop_start()
#    clientA.publish("devices/" + device_id +
#                    "/messages/events/",
#                    payload="{\"WIMMS/EM63/@ActSimPara1\":23}", qos=1)
    clientA.publish("devices/" + device_id +
                    "/messages/events/",
                    payload=messageA, qos=1)
    clientA.loop_stop()


topicstr1 = "WIMMS/EM63/DATE"
payload1 = ""
topicstr2 = "WIMMS/EM63/TIME"
payload2 = ""
topicstr3 = "WIMMS/EM63/@ActSimPara1"
payload3 = 3
topicstr4 = "WIMMS/EM63/@ActSimPara2"
payload4 = 4
topicstr5 = "WIMMS/EM63/ActCntCyc"
payload5 = ""
topicstr6 = "WIMMS/EM63/ActCntPrt"
payload6 = ""
topicstr7 = "WIMMS/EM63/ActStsMach"
payload7 = ""
topicstr8 = "WIMMS/EM63/ActTimCyc"
payload8 = ""
topicstr9 = "WIMMS/EM63/SetCntMld"
payload9 = ""
topicstr10 = "WIMMS/EM63/SetCntPrt"
payload10 = ""
# MSG_TXT = "{\"%s\": %s,\"%s\": %s}"
# payload1=0
# payload2=0


# MQTT parameters for Azure IoT Hub; replaces connectionstring
device_key = ''  # primary key of device
iot_hub_name = ''  # Name of IoT Hub
device_id = ''  # Name of device to connect to
sas_token = ''  # SAS token
cc_config_file = 'keys.json'
path_to_root_cert = "digicert.cer"
enable_cloud_conn = os.getenv("ENABLE_CLOUD_CONNECTION", "False")

if enable_cloud_conn == "True":
	r = cc_config(cc_config_file)
	if r > 0:
		sys.exit(1)
else:
	print("Cloud connection disabled. Not reading json.keys. ENABLE_CLOUD_CONNECTION = {}".format(enable_cloud_conn))


# Data input from MQTT broker
broker_host = os.getenv("MQTT_BROKER_HOST", "127.0.0.1")
broker_port = os.getenv("MQTT_BROKER_PORT", 1883)


listetopic = []
listepayload = []
# TODO we should retry and wait here until the broker is ready
# this might take a couple of seconds in real deployments
clientB = paho.Client("CC-Client-Sub")
clientB.on_message = on_message
print("---------------------------------------------")
print("Connecting to MQTT broker: {}:{}".format(broker_host, broker_port))
clientB.connect(broker_host, port=int(broker_port))
# print("Subscribing to topic","WIMMS/EM63/TIME")
# client.subscribe("WIMMS/EM63/TIME")
print("Subscribing to MQTT broker's topic", "WIMMS/EM63/#")
print("---------------------------------------------")
clientB.subscribe("WIMMS/EM63/#")


# MQTT for Azure IoT Hub
if enable_cloud_conn == "True":
	clientA = azure_mqtt.Client(client_id=device_id, protocol=azure_mqtt.MQTTv311)
	clientA.on_connect = on_connectA
	clientA.on_disconnect = on_disconnectA
	clientA.on_publish = on_publishA
	clientA.username_pw_set(username=iot_hub_name +
							".azure-devices.net/" + device_id, password=sas_token)
	clientA.tls_set(ca_certs=None,
					certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
					tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
	# clientA.tls_set(ca_certs=path_to_root_cert,
	#                 certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
	#                 tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
	clientA.tls_insecure_set(False)
	clientA.connect(iot_hub_name+".azure-devices.net", port=8883)
else:
	print("Cloud connection disabled. Not connecting to Azure. ENABLE_CLOUD_CONNECTION = {}".format(enable_cloud_conn))
	
sys.stdout.flush()
sys.stderr.flush()

while True:
    print("---------------------------------------------")
    # Subscribe from broker
    clientB.loop_start()
    time.sleep(1)
    clientB.loop_stop()
    sys.stdout.flush()
# client.loop_forever()
