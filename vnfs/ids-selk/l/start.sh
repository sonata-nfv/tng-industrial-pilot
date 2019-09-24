#!/bin/bash

export IP=`env | grep e_vnf3_eu_5gtango_0_6_elastic9200_ip | cut -d "=" -f 2`
echo $IP

export ELASTICSEARCH_HOSTS=http://$IP:9200
echo $ELASTICSEARCH_HOSTS

bin/logstash
