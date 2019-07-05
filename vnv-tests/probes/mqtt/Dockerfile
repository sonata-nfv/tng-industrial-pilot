FROM golang:1.11

LABEL maintainer="Aureliano Sinatra <sinaure@gmail.com>"

ENV PROBE "mqttprobe"

RUN git config --global http.sslVerify false
RUN go get github.com/krylovsk/mqtt-benchmark

ADD entrypoint.sh /app/
ADD config.cfg /app/

ENTRYPOINT [ "/app/entrypoint.sh" ]