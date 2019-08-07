# Mqtt Probe

This probe executes a stress test against a broker IP:PORT. It generates a results.log file in /output that can be accessed via docker volume


| Parameter | Mandatory |
|---|---|
|IP| Yes|
|PORT| Yes|
## Local execution example
	make build
	make run ip=192.168.99.100 port=1883