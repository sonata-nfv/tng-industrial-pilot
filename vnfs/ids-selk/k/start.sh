#!/bin/bash
export IP=`env | grep EU_5GTANGO_E_VNF3_0_4 | grep 9200_TCP_ADDR | cut -d "=" -f 2`
export ELASTICSEARCH_HOSTS=http://$IP:9200
bin/kibana -e http://$IP:9200

