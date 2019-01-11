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
    File name: MDC_VNF.py
    Author: Marcel Müller, Weidmüller Group, Detmold, Germany
    E-Mail: Marcel.Mueller@weidmueller.com
    Description: Machine Data Collector
    Version: 2018-12-21
    Python Version 3.6.7
    Editor: Spyder (indentation characters: tabulations)
    Maintainer: Marcel Müller
    Copyright: Copyright 2018, Marcel Müller, Weidmüller Group, Detmold, Germany
"""
"""   
    Modules needed
    # pip3 install paho-mqtt --user
"""
"""
    ToDO
    SAMBA server
    FTP server
    Test with physical machine
"""
"""
    README
    Run an MQTT broker, e.g., mosquitto.
    MDC_VNF publishes to it: localhost:1883 (unsecured)
    If mosquitto is your broker, you can check your published messages with: $~ mosquitto_sub -t "#" -v 
    or a graphical mqtt client, e.g., mqttfx.
"""

#import datetime
import os
import time
import signal
import sys
import traceback
import paho.mqtt.client as paho
from em63 import rmFile 
# see http://www.steves-internet-guide.com/client-objects-python-mqtt/
# see http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
# -------------------------------------------------------------------------- #
# Configuration
# -------------------------- Primary --------------------------------------- #
#
# Name of the machine
machinename = "WIMMS"
# Session number
session = "0001" 
# Path to the Euromap 63 sharing folder for this machine
# get configuration from environment varialbe (or use the old default)
filepath = os.environ.get("MDC_EM63_SHARE_FOLDER", "/home/marcel/em63/")
# MQTT broker
broker = os.environ.get("MQTT_BROKER_HOST", "127.0.0.1")
broker_port = os.environ.get("MQTT_BROKER_PORT", 1883)

# -------------------------- Secondary-------------------------------------- #
#
# Job number: Initial value for job is 0, in while it is incremented
job = 0;
# Cycle Time
waitTimeCycle=2.0 # attention: 1 seems to small for emulator deployment
# Loops and Time per loop for waiting for machine's answer: DAT file
waitCnt=100; # 10 times
waitTime=0.1; # 1 second

stop_loop = False  # stop flag


# allow graceful stop
def signal_handler(sig, frame):
    global stop_loop
    stop_loop = True
    print('Received signal. Stopping ...')
    exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
#
#
# -------------------------------------------------------------------------- #


jobFileHeaderStatic="""START IMMEDIATE
STOP NEVER
SAMPLES 1
SESSIONS 1
PARAMETERS
"""

# Define the parameters which have to be checked
parameterfile="parameter.em63"
# If no file with parameters is available the machine status is checked
print("---------------------------------------------")
print("Machine defined: ", machinename)
print("Path defined: ", filepath)
if os.path.exists(parameterfile):
    print("Use ", parameterfile)
    try:
        f_in = open(parameterfile,'r')
        jobFileBody = f_in.read()
    finally:
        f_in.close()
else:
    print("Can not find ", parameterfile)
    jobFileBody ="ActStsMach;"

mqttclientname = machinename + "-client-pub"
client = paho.Client(mqttclientname)



# # # Cyclic part
while not stop_loop:
    sys.stdout.flush()
    try: 
        if job >=999:
            job=1
        else:
            job=job+1;
            
        try:
            # MQTT connection
            print("Connecting to broker ", broker)
            client.connect(broker, port=int(broker_port))
            print("Connected.")
        except BaseException as ex:
            print("Cannot connect to MQTT broker '{}:{}': {}".format(broker, broker_port, ex))
        
        # Delete *.RSP if available
        rspFile = os.path.join(filepath, "SESS" + session + '.RSP')
        rmFile(rspFile)
        # Delete *.DAT if available
        datFile = os.path.join(filepath, session + str(job).zfill(4) + '.DAT')
        rmFile(datFile)
        # Delete *.LOG if available
        logFile = os.path.join(filepath, session + str(job).zfill(4) + '.LOG')
        rmFile(logFile)
        
        # Create new *.JOB
        jobFile = os.path.join(filepath, session + str(job).zfill(4) + '.JOB')
        f_jobFile = open(jobFile, 'w+')
        jobFileHeaderDynamic1='JOB 0000' + str(job).zfill(4) + ' RESPONSE "' + session + str(job).zfill(4) + '.LOG";\n'
        jobFileHeaderDynamic2='REPORT ' + session + '_0000' + str(job).zfill(4) + ' REWRITE "' + session + str(job).zfill(4) + '.DAT"\n'
        jobFileHeader=jobFileHeaderDynamic1 + jobFileHeaderDynamic2 + jobFileHeaderStatic
        jobFileContent = jobFileHeader + jobFileBody
        f_jobFile.write(jobFileContent)
        f_jobFile.close()

        # Create new *.REQ
        reqFile= os.path.join(filepath, "SESS" + session + '.REQ')
        f_reqFile = open(reqFile, 'w+')
        reqFileContent = '0000' + str(job).zfill(4) + ' EXECUTE "' + session + str(job).zfill(4) + '.JOB";'
        f_reqFile.write(reqFileContent)
        f_reqFile.close()

        print("JOB file and Request file are created:") 
        print("Job file: ", jobFile)
        print("REQ file: ", reqFile)

        # Wait seconds for each cycle between requesting and using *.DAT file
        time.sleep(waitTimeCycle); 
        
        # File *.DAT which have to be used
        datFile = os.path.join(filepath, session + str(job).zfill(4) + '.DAT')
        print("Looking for: ",datFile)

        # Open *.DAT file
        file_found = False
        waitIndex=0
        while waitIndex<waitCnt:
            if os.path.exists(datFile):
                # also check that file is not empty to be more robust
                with open(datFile,'r') as f:
                    if len(f.read()) > 0:
                        print("DAT file found. Processing ...")
                        file_found = True
                        break
            else:
                waitIndex=waitIndex+1;
                print("Waiting ({}/{})".format(waitIndex, waitCnt))
                sys.stdout.flush()
                time.sleep(waitTime)
        if not file_found:
            # ok never stop in a real deployment, just retry. give other VNFs time to breathe ;-)
            print("Error no Euromap 63 response file was found! Retry!")
            continue
       
        f_in = open(datFile,'r')
        parameter_value_list_in = f_in.read()
        f_in.close() #2 can not be closed later because of it will be removed in a few lines later
        
        # Generate timestamp UTC
        # utc_datetime = datetime.datetime.utcnow()
        # zeitstempel = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
        # print(parameter_value_list_in)
        parameter_value_list = parameter_value_list_in.splitlines()
        if len(parameter_value_list) < 1:
            print("Error: parameter_value_list was empty. Retry!")
            continue
        parameter_str = parameter_value_list[0]
        value_str = parameter_value_list[1]
        parameterlist = parameter_str.split(',')
        valuelist = value_str.split(',')

        # Make sure, that parameters like x[y,z] are useable, otherwise you have x[ in entry 1 and z] in entry 2.
        if len(parameterlist) != len(valuelist):
            for index in range(len(parameterlist)):
                if '[' in parameterlist[index] and ']' not in parameterlist[index]:
                    parameterlist[index] = parameterlist[index] + ',' + parameterlist[index+1]
                elif ']' in parameterlist[index] and '[' not in parameterlist[index]:
                    parameterlist[index] = ""
        parameterlist_final = list(filter(None, parameterlist))

        # Required for Version Descriptions
        # Version numbers use commas and space is used in date+time
        # For parameters, we have looked for empty entries to remove it
        # For values it is not possible because values could be empty
        delDummy="-.-"
        delDummyCnt=0;
        if len(parameterlist_final) != len(valuelist):
            for index in range (len(valuelist)):
                if ' (r' in valuelist[index]:
                    valuelist[index-1]=valuelist[index-1]+valuelist[index]
                    valuelist[index]=delDummy
                    delDummyCnt+=1
            for index in range(delDummyCnt): 
                valuelist.remove(delDummy)
        valuelist_final = valuelist

        try:
            start_ende = len(parameterlist_final)
            if start_ende == len(valuelist_final):
                print("Start transfer: publishing...")
                for index in range(len(parameterlist_final)):
                    print("#" + str(index) + "\t : \t"  + parameterlist_final[index] + "\t\t" + valuelist_final[index])
                client.loop_start()
                for index in range(start_ende):
                    parameter = parameterlist_final[index]
                    value = valuelist_final[index]
                    parameterName = machinename + "/EM63/" +  parameter
                    parameterValue = str(value)
                    #(topic, payload)
                    client.publish(parameterName,parameterValue)
            else:
                print("Number of parameters and values is not equal")
                print("Number of parameters: ", len(parameterlist_final))
                print("Number of values: ", len(valuelist))
            client.disconnect() #disconnect
            client.loop_stop() #stop loop
        except BaseException as ex:
            print("Publish error: {}".format(ex))
    
        # After each cycle: remove all files
        rmFile(rspFile)
        rmFile(datFile)
        rmFile(logFile)
        rmFile(jobFile)
        rmFile(datFile)
        print("---------------------------------------------")
    except BaseException as ex:
        print("Exception detected: {}".format(ex))
        traceback.print_exc()
        time.sleep(1)
    finally:
        f_in.close() #2 close opened *.DAT
        client.disconnect() #disconnect
        client.loop_stop() #stop loop
