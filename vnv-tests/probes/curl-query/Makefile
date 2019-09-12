build:
	docker build -t easyglobalmarket/curl-probe .
build-nc:
	docker build --no-cache -t easyglobalmarket/curl-probe .	
push:
	docker push easyglobalmarket/curl-probe	
run:
	docker run --rm --net=egm -e "IP=http://192.168.99.100" -e "PORT=9090" -e "APIPATH=/api/v1/query?query=" -e "QUERY=em63_actcntcyc"   --name curl-probe --net=egm easyglobalmarket/curl-probe
stop:
	docker stop curl-probe
	docker rm curl-probe
