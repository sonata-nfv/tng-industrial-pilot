#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
    File name: CCA_VNF.py
    Author: Marcel Müller, Weidmüller Group, Detmold, Germany
    E-Mail: Marcel.Mueller@weidmueller.com
    Description: Cloud Connector Azure
    Version: 2019-01-07
    Python Version 3.6.7
    Editor: Spyder (indentation characters: tabulations)
    Maintainer: Marcel Müller
    Copyright: Copyright 2018, Marcel Müller, Weidmüller Group, Detmold, Germany
    Status: CONFIDENTIAL, only for internal purposes, DO NOT PUBLISH
"""
""" Modules needed
    pip3 install azure-iothub-device-client --user
    sudo apt-get install libboost-python-dev
    synaptic: libboost-all-dev, python3-azure
    libboost1.58 required
"""
""" TODO
    Sends a telegram to Azure per parameter. Better: Send a set of parameters per telegram.
"""
import time
import os
import sys
import json
import paho.mqtt.client as paho
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
from datetime import datetime


# IoT Hub function
def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

# IoT Hub function
def iothub_client_init(azure_conn_string):
    if azure_conn_string is None:
        print("Error: Azure connection string is None.")
        return None
    client = IoTHubClient(azure_conn_string, IoTHubTransportProvider.MQTT)
    return client

# MQTT function
def on_message(client, userdata, message):
    global payload3, payload4
    payload_str = str(message.payload.decode("utf-8"))
    topic_str = str(message.topic)
    msgstr = build_message(topic_str, payload_str)
    
    if topic_str == topicstr3:
        payload3=float(payload_str)
    if topic_str == topicstr4:
        payload4=float(payload_str)
        
    
    if msgstr!=0:
        send_message(msgstr)
        
        
def build_message(topic, payload):
    global listetopic, listepayload
    print("Received message: Topic: %s Payload: %s" % (topic, payload))
    
    if topic in listetopic:
        msgstr = "{"
        for index in range(len(listetopic)):
            msgstr += "\"%s\": %s" % (str(listetopic[index]), str(listepayload[index]))
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
        #return msgdict
    else:
        listetopic.append(topic)
        listepayload.append(payload)
        return 0
        
def send_message(msg):
    global payload3, payload4
    #print("RAW message: %s" % msg)  
    
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
    #topicstr1 = "WIMMS/EM63/DATE"
    #topicstr2 = "WIMMS/EM63/@ActSimPara2"
    
    MSG_TXT = "{\"%s\": %.2f,\"%s\": %.2f}"
    #payload3=12
    #payload4=2*payload3
    msg_txt_formatted = MSG_TXT % (topicstr3, payload3, topicstr4, payload4)
    messageA = IoTHubMessage(msg_txt_formatted)
    if clientA:
        print("Sending message: %s \n" % messageA.get_string() )
        clientA.send_event_async(messageA, send_confirmation_callback, None)
    else:
        print("Skipping message to Azure. Not connected.")

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
#MSG_TXT = "{\"%s\": %s,\"%s\": %s}"
#payload1=0
#payload2=0
    
#Data output to Microsoft Azure using the MQTT protocol: clientA

#
# Azure connection configuration
#
azure_conn_string_file = os.getenv("AZURE_SECRET_FILE",
                                     "azure_connection_string.secret")
azure_conn_string = None
try:
    with open(azure_conn_string_file, "r") as f:
        print("Loading Azure connection string from: {}"
              .format(azure_conn_string_file))
        azure_conn_string = f.read().strip()
        if azure_conn_string.startswith("<TODO"):
            raise BaseException("Azure connection string not configured!")
        print("Azure connection string successfully loaded.")
except BaseException as ex:
    azure_conn_string = None
    print("Couldn't load Azure connection string from: {}. Error: {}"
          .format(azure_conn_string_file, ex))

# Data input from MQTT broker
broker_host = os.getenv("MQTT_BROKER_HOST", "127.0.0.1")
broker_port = os.getenv("MQTT_BROKER_PORT", 1883)

listetopic = []
listepayload = []
# TODO we should retry and wait here until the broker is ready
# this might take a couple of seconds in real deployments
clientB = paho.Client("CC-Client-Sub")
clientB.on_message = on_message
print("Connecting to broker: {}:{}".format(broker_host, broker_port))
clientB.connect(broker_host, port=int(broker_port))
#print("Subscribing to topic","WIMMS/EM63/TIME")
#client.subscribe("WIMMS/EM63/TIME")
print("Subscribing to topic", "WIMMS/EM63/#")
clientB.subscribe("WIMMS/EM63/#")
clientA = iothub_client_init(azure_conn_string)
sys.stdout.flush()
sys.stderr.flush()
while True:
    clientB.loop_start()
    time.sleep(1)
    clientB.loop_stop()
    sys.stdout.flush()
#client.loop_forever()