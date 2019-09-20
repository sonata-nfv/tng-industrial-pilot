#!/usr/bin/env python3

from flask import Flask, request, json
import time
import logging
import glob
import ipaddress
import os

app = Flask(__name__)

lastInvocationTime = None
@app.route("/stats", methods=["GET"])
def stats():
    global lastInvocationTime
    mytime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    response = {}

    files = []
    files = glob.glob("/var/log/logstash/*.json")
    files.sort()
    if files.count == 0:
        response["resource_id"] = os.getenv("HOSTNAME")
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
    alarmedIPs["resource_id"] = os.getenv("HOSTNAME")
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
    return json.dumps(alarmedIPs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
