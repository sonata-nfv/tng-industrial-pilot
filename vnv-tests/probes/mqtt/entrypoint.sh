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
echo "rounds = $ROUNDS"
echo "qos = $QOS"

echo "******* mqttprobe: executing benchmark *******"

for i in $( eval echo {1..$ROUNDS} )
do
    echo "Executing round $i"
    mqtt-benchmark --broker tcp://$IP:$PORT --count $(( COUNT * i )) --size $(( SIZE * i )) --clients $(( CLIENTS * i )) --qos $QOS --format json --username $USERNAME --password $PASSWORD > $RESULTS_FILE
done

echo "output redirect to: $RESULTS_FILE"
