FROM alpine

LABEL maintainer="Aureliano Sinatra <sinaure@gmail.com>"

ENV INSTALL_PATH /prometheus-query
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN apk add --no-cache curl jq

ENV PROBE "prometheus-query"
ADD entrypoint.sh $INSTALL_PATH
ADD config.cfg $INSTALL_PATH


ENTRYPOINT [ "/prometheus-query/entrypoint.sh" ]