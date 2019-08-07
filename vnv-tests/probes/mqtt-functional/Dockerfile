FROM python:3.7.2-slim

LABEL maintainer="Aureliano Sinatra <sinaure@gmail.com>"


ENV INSTALL_PATH /mqtt-functional-probe
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN apt update
RUN apt install -y python3-pip python3-dev libcurl4-gnutls-dev librtmp-dev git
RUN apt install -y jq 
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD entrypoint.sh $INSTALL_PATH
ADD config.cfg $INSTALL_PATH
ADD input.txt $INSTALL_PATH


ENTRYPOINT [ "/mqtt-functional-probe/entrypoint.sh" ]