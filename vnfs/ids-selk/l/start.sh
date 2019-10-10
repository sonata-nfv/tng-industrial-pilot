#!/bin/bash

export IP=`env | grep e_vnf3_eu_5gtango | grep elastic9200_ip | cut -d "=" -f 2`
echo $IP

export ELASTICSEARCH_HOSTS=$IP:9200
echo $ELASTICSEARCH_HOSTS

#sed -i "s/\${ELASTICSEARCH_HOSTS}/$ELASTICSEARCH_HOSTS/g" ./config/logstash.yml

bin/logstash
