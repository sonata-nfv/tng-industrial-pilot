#!/bin/bash

echo "******* mqttprobe: starting entrypoint.sh ******"

source /app/config.cfg

echo "******* mqttprobe: creating folder /output/${PROBE}/${HOSTNAME} *******"

mkdir -p /output/${PROBE}/${HOSTNAME}

echo "ip = $IP"
echo "port = $PORT"
echo "packet size = $SIZE"
echo "messages per client = $COUNT"
echo "clients = $CLIENTS"

echo "******* mqttprobe: executing benchmark *******"

mqtt-benchmark --broker tcp://$IP:$PORT --count $COUNT --size $SIZE --clients $CLIENTS --qos 2 --format json --username $USERNAME --password $PASSWORD > $RESULTS_FILE

echo "output redirect to: $RESULTS_FILE"
