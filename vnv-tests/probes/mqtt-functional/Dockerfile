FROM golang:1.11

LABEL maintainer="Aureliano Sinatra <sinaure@gmail.com>"

ENV PROBE "mqttprobe-functional"

RUN git config --global http.sslVerify false
RUN go get https://github.com/sinaure/mqtt-benchmark.git

ADD entrypoint.sh /app/
ADD config.cfg /app/

ENTRYPOINT [ "/app/entrypoint.sh" ]