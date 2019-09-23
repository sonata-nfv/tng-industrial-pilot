#!/bin/bash

export VERSION=`echo $1 | tr '.' '_'`
echo $VERSION

export LIP=`env | grep EU_5GTANGO_LHC_VNF2_$VERSION | grep PORT_5044_TCP_ADDR | cut -d "=" -f 2`
export LOGSTASH_HOSTS=$LIP:5044
echo $LOGSTASH_HOSTS

export KIP=`env | grep EU_5GTANGO_K_VNF4_$VERSION | grep PORT_5601_TCP | cut -d "=" -f 2`
export KIBANA_HOST=$KIP:5601
echo $KIBANA_HOST

filebeat -e
