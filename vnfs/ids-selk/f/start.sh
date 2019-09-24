#!/bin/bash

export LIP=`env | grep lhc_vnf2_eu_5gtango_0_6_logstash5044_ip | cut -d "=" -f 2`
export LOGSTASH_HOSTS=$LIP:5044
echo $LOGSTASH_HOSTS

export KIP=`env | grep k_vnf4_eu_5gtango_0_6_kibana5601_ip | cut -d "=" -f 2`
export KIBANA_HOST=$KIP:5601
echo $KIBANA_HOST

filebeat -e
