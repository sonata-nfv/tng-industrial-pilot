build:
	docker build -t easyglobalmarket/mqtt-functional-probe .
push:
	docker push easyglobalmarket/mqtt-functional-probe	
run:
	docker run --name mqtt-functional-probe --rm -e "IP=192.168.99.100" -e "PORT=1883" -e "BULK_DATA=$(bulk_data)"  easyglobalmarket/mqtt-functional-probe	
stop:
	docker stop easyglobalmarket/mqtt-functional-probe || true
	docker rm easyglobalmarket/mqtt-functional-probe || true
	
	