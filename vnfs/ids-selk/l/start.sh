#!/bin/bash
export VERSION=`echo $1 | tr '.' '_'`
echo $VERSION

export IP=`env | grep EU_5GTANGO_E_VNF3_$VERSION | grep PORT_9200_TCP_ADDR | cut -d "=" -f 2`
echo $IP

export ELASTICSEARCH_HOSTS=http://$IP:9200
echo $ELASTICSEARCH_HOSTS

bin/logstash
