build:
	docker build -t easyglobalmarket/mqtt-probe .
push:
	docker push easyglobalmarket/mqtt-probe	
run:
	docker run  -e "IP=$(ip)" -e "PORT=$(port)" -e "QOS=0" -e "CLIENTS=$(clients)" -e "COUNT=$(count)" -e "MESSAGE=$(message)"  --name docker-mqtt-probe --net=egm easyglobalmarket/mqtt-probe
stop:
	docker stop docker-mqtt-probe
	docker rm docker-mqtt-probe
