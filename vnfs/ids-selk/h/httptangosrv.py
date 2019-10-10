#!/usr/bin/env python3

from flask import Flask, request, json
from time import sleep
import time
import logging
import glob
import ipaddress
import os

app = Flask(__name__)

lastInvocationTime = None
lastInvocationTimeForLogins = None

@app.route("/login", methods=["GET"])
def logins():
    global lastInvocationTimeForLogins
    mytime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    response = {}

    files = []
    files = glob.glob("/var/log/logstash/*.log")
    files.sort()
    if files.count == 0:
        response["resource_id"] = os.getenv("container_name")
        alarmedIPs["login_tried"] = "0"
        alarmedIPs["login_successfull"] = "0"
        return json.dumps(response)

    name = "login-" + mytime
    if lastInvocationTimeForLogins is not None:
        nameStart = "event-" + lastInvocationTimeForLogins
    selectedFiles = []

    if lastInvocationTimeForLogins is None:
        for f in files:
            if f.split('/')[len(f.split('/')) - 1] < name:
                selectedFiles.append(f)
    else:
        for f in files:
            if (f.split('/')[len(f.split('/')) - 1] > nameStart) and (f.split('/')[len(f.split('/')) - 1] < name):
                selectedFiles.append(f)

    events = []
    dJson = {}
    for f in selectedFiles:
        with open(f, 'r') as evFile:
            for cnt, line in enumerate(evFile):
                dJson = json.loads(line)
                events.append(dJson)
            evFile.close()

    alarmedIPs = {}
    alarmedIPs["resource_id"] = os.getenv("container_name")
    login_tried = 0
    login_successfull = 0
    flowId = 0
    if len(events) == 0:
        alarmedIPs["login_tried"] = "0"
        alarmedIPs["login_successfull"] = "0"
    else:
        for ev in events:
            if ev['smb']['command']:
                print("command = ", ev['smb']['command'])
                if(ev['smb']['command'] == 'SMB1_COMMAND_SESSION_SETUP_ANDX'):
                    alarmedIPs["login_tried"] = str(++login_tried)
                else:
                    if(ev['smb']['command'] == 'SMB1_COMMAND_TRANS'):
                        if flowId != ev['flow_id']:
                            alarmedIPs["login_successfull"] = str(++login_successfull)
                            flowId = ev['flow_id']

    lastInvocationTimeForLogins = mytime
    return json.dumps(alarmedIPs)

@app.route("/stats", methods=["GET"])
def stats():
    global lastInvocationTime
    mytime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    response = {}

    files = []
    files = glob.glob("/var/log/logstash/*.json")
    files.sort()
    if files.count == 0:
        response["resource_id"] = os.getenv("container_name")
        alarmedIPs["ip0"] = "0"
        return json.dumps(response)

    name = "event-" + mytime
    if lastInvocationTime is not None:
        nameStart = "event-" + lastInvocationTime
    selectedFiles = []

    if lastInvocationTime is None:
        for f in files:
            if f.split('/')[len(f.split('/')) - 1] < name:
                selectedFiles.append(f)
    else:
        for f in files:
            if (f.split('/')[len(f.split('/')) - 1] > nameStart) and (f.split('/')[len(f.split('/')) - 1] < name):
                selectedFiles.append(f)

    events = []
    dJson = {}
    for f in selectedFiles:
        with open(f, 'r') as evFile:
            for cnt, line in enumerate(evFile):
                dJson = json.loads(line)
                events.append(dJson)
            evFile.close()

    alarmedIPs = {}
    alarmedIPs["resource_id"] = os.getenv("container_name")
    ipcount = 0
    if len(events) == 0:
        alarmedIPs["ip0"] = "0"
    else:
        for ev in events:
            print("ip = ", int(ipaddress.ip_address(str(ev['dest_ip']))))
            if(int(ipaddress.ip_address(str(ev['dest_ip']))) not in alarmedIPs.values()):
                alarmedIPs["ip" + str(ipcount)] = str(int(ipaddress.ip_address(ev['dest_ip'])))
                ++ipcount

    lastInvocationTime = mytime
    sleep(15)
    return json.dumps(alarmedIPs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
