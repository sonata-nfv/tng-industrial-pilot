build:
	docker build -t easyglobalmarket/mqtt-functional-probe .
push:
	docker push easyglobalmarket/mqtt-functional-probe	
run:
	docker run --name mqtt-functional-probe --rm -e "IP=$(ip)" -e "PORT=$(port)"  easyglobalmarket/mqtt-functional-probe	
stop:
	docker stop easyglobalmarket/mqtt-functional-probe || true
	docker rm easyglobalmarket/mqtt-functional-probe || true
	
	