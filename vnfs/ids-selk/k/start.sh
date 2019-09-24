#!/bin/bash

export IP=`env | grep e_vnf3_eu_5gtango | grep elastic9200_ip | cut -d "=" -f 2`
export ELASTICSEARCH_HOSTS=http://$IP:9200
echo $ELASTICSEARCH_HOSTS

bin/kibana -e http://$IP:9200

