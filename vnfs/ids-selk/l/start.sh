#!/bin/bash
export IP=`env | grep EU_5GTANGO_E_VNF3_0_4 | grep 9200_TCP_ADDR | cut -d "=" -f 2`
echo $IP
export ELASTICSEARCH_HOSTS=http://$IP:9200
bin/logstash --verbose
