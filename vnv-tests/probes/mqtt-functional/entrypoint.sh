#!/bin/bash

echo "******* mqttprobe: starting entrypoint.sh ******"

source /mqtt-functional-probe/config.cfg

echo "******* mqttprobe: creating folder /output/${PROBE}/${HOSTNAME} *******"

mkdir -p /output/${PROBE}/${HOSTNAME}

echo "ip = $IP"
echo "port = $PORT"

echo "******* mqttprobe: executing benchmark *******"

for k in $(jq -r '.[] | [ .topic, .value|tostring ] | join(";")' <<< "$BULK_DATA"); do
	echo $k
	array= ${k//;/ }
	topic="$(echo $k | cut -d';' -f1)"
	value="$(echo $k | cut -d';' -f2)"
	echo "topic: $topic"
	echo "value: $value"
	mqtt-bench publish --host $IP --port $PORT --topic $topic  --message $value --username 'hub-iot' --password 'hub-iot'>> $RESULTS_FILE
done

echo "output redirect to: $RESULTS_FILE"
