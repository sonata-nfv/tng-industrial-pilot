build:
	docker build -t easyglobalmarket/prometheus-curl-probe .
build-nc:
	docker build --no-cache -t easyglobalmarket/prometheus-curl-probe .	
push:
	docker push easyglobalmarket/prometheus-curl-probe	
run:
	docker run --rm --net=egm -e "IP=http://192.168.99.100" -e "PORT=9090" -e "QUERY=em63_actcntprt"   --name prometheus-curl-probe --net=egm easyglobalmarket/prometheus-curl-probe
stop:
	docker stop prometheus-curl-probe
	docker rm prometheus-curl-probe
