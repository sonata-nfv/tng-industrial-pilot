#!/bin/bash

echo "******* mqttprobe: starting entrypoint.sh ******"

source /mqtt-functional-probe/config.cfg

echo "******* mqttprobe: creating folder /output/${PROBE}/${HOSTNAME} *******"

mkdir -p /output/${PROBE}/${HOSTNAME}

echo "ip = $IP"
echo "port = $PORT"

echo "******* mqttprobe: executing benchmark *******"
delim=' '
input="/mqtt-functional-probe/input.txt"
while IFS= read -r line
do
  echo "$line"
  read -a strarr <<< "$line"
  echo "topic: ${strarr[0]}"
  echo "value: ${strarr[1]}"
  mqtt-bench publish --host $IP --port $PORT --topic ${strarr[0]}  --message ${strarr[1]} --username 'hub-iot' --password 'hub-iot'>> $RESULTS_FILE
done < "$input"



echo "output redirect to: $RESULTS_FILE"
