#!/bin/bash

export LIP=`env | grep EU_5GTANGO_LH_VNF2_0_4 | grep 5044_TCP_ADDR | cut -d "=" -f 2`
export LOGSTASH_HOSTS=$LIP:5044

export KIP=`env | grep EU_5GTANGO_K_VNF4_0_4 | grep 5601_TCP_ADDR | cut -d "=" -f 2`
export KIBANA_HOSTS=http://$KIP:5601

filebeat -e
