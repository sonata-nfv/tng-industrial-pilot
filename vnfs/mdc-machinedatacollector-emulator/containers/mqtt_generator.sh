#!/bin/bash

# simple shell script that periodically publishes MQTT messages

# ENV variables come from Dockerfile, the following is for debugging only
# MQTT_BROKER_HOST=127.0.0.1
# MQTT_BROKER_PORT=18831
# TOPIC=machines/molding-042/sensors/temp

while :
do
    VALUE=$RANDOM
    mosquitto_pub -h $MQTT_BROKER_HOST -p $MQTT_BROKER_PORT -t $TOPIC -m $VALUE
    echo "Published on $TOPIC: $VALUE"
    sleep 1  # publish once per second
done
