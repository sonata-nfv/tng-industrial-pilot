# Default configuration of CC_VNF

## General configuration
Container: see Dockerfile for environment variables

# Application of MDC
Run an MQTT broker, e.g., mosquitto.
CC_VNF subscribes from it.
Local (default): localhost:1883 (unsecured)

## Manual start of MDC_VNF
```sh
$~ python3 CC_VNF.py
```

# Modules needed
```sh
$~ pip3 install paho-mqtt --user
```

# TODO
Json with MQTT config statt string
Sends a telegram to Azure per parameter. Better: Send a set of parameters per telegram.

