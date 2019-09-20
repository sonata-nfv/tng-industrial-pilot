#!/bin/bash

export VERSION=`echo $1 | tr '.' '_'`; echo $VERSION

export LIP=`env | grep 5gtango_$VERSION | grep 5044_ip | cut -d "=" -f 2`
export LOGSTASH_HOSTS=$LIP:5044
echo $LOGSTASH_HOSTS

export KIP=`env | grep 5gtango_$VERSION | grep 5601_ip | cut -d "=" -f 2`
export KIBANA_HOST=$KIP:5601
echo $KIBANA_HOST

#filebeat -e
