FROM python:3.7.2-slim

LABEL maintainer="Aureliano Sinatra <sinaure@gmail.com>"

ENV INSTALL_PATH /prometheus-query
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN apt update
RUN apt install -y  curl
RUN apt install -y jq 

ENV PROBE "prometheus-query"
ADD entrypoint.sh $INSTALL_PATH
ADD config.cfg $INSTALL_PATH


ENTRYPOINT [ "/prometheus-query/entrypoint.sh" ]