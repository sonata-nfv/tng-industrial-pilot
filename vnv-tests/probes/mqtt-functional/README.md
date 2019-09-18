# Mqtt Probe

This probe executes a stress test against a broker IP:PORT. It generates a results.log file in /output that can be accessed via docker volume


| Parameter | Mandatory |
|---|---|
|IP| Yes|
|PORT| Yes|
|BULK_DATA| Yes|
## Local execution example
	make build
	make run 

	