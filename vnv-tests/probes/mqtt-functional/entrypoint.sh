#!/bin/bash

echo "******* mqttprobe: starting entrypoint.sh ******"

source /app/config.cfg

echo "******* mqttprobe: creating folder /output/${PROBE}/${HOSTNAME} *******"

mkdir -p /output/${PROBE}/${HOSTNAME}

echo "ip = $IP"
echo "port = $PORT"
echo "payload = $MESSAGE"
echo "messages per client = $COUNT"
echo "clients = $CLIENTS"
echo "qos = $QOS" 

echo "******* mqttprobe: executing benchmark *******"

mqtt-bench publish --host $IP --port $PORT --topic $TOPIC --qos $QOS --thread-num $CLIENTS --publish-num $COUNT --message $MESSAGE > $RESULTS_FILE

echo "output redirect to: $RESULTS_FILE"
