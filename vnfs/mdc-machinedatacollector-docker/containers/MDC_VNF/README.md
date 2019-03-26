# Default configuration of MDC_VNF

## General configuration
Local: default EM63 shared session folder: /home/marcel/em63/
Container: see Dockerfile for environment variables

# Application of MDC
Run an MQTT broker, e.g., mosquitto.
MDC_VNF publishes to it.
Local (default): localhost:1883 (unsecured)
If mosquitto is your broker, you can check your published messages with: 
```sh
$~ mosquitto_sub -t "#" -v 
```
or a graphical mqtt client, e.g., mqttfx.

## Manual start of MDC_VNF
```sh
$~ python3 MDC_VNF.py
```

# Modules needed
```sh
$~ pip3 install paho-mqtt --user
```

# TODO
Using FTP server instead of samba server.
Test with real physical machine.
