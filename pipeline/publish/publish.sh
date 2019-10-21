#!/bin/bash
set -e

# vimemu images
docker push sonatanfv/vnf-dt:vimemu
docker push sonatanfv/vnf-mdc:vimemu
docker push sonatanfv/vnf-rtr-nat:vimemu
docker push sonatanfv/vnf-cc-broker:vimemu
docker push sonatanfv/vnf-cc-processor:vimemu
docker push sonatanfv/vnf-cc-mqttexporter:vimemu
docker push sonatanfv/vnf-cc-database:vimemu
docker push sonatanfv/vnf-eae:vimemu

# kubernetes images
docker push sonatanfv/vnf-dt:k8s
docker push sonatanfv/vnf-mdc:k8s
docker push sonatanfv/vnf-cc-broker:k8s
docker push sonatanfv/vnf-cc-processor:k8s
docker push sonatanfv/vnf-cc-mqttexporter:k8s
docker push sonatanfv/vnf-cc-database:k8s
docker push sonatanfv/vnf-eae:k8s
docker push sonatanfv/vnf-ids-suricata:k8s
docker push sonatanfv/vnf-ids-filebeat:k8s
docker push sonatanfv/vnf-ids-logstash:k8s
docker push sonatanfv/vnf-ids-http:k8s
docker push sonatanfv/vnf-ids-elasticsearch:k8s
docker push sonatanfv/vnf-ids-kibana:k8s
docker push sonatanfv/vnf-proxyvpn:k8s

docker push sonatanfv/vnf-dt:latest
docker push sonatanfv/vnf-mdc:latest
docker push sonatanfv/vnf-cc-broker:latest
docker push sonatanfv/vnf-cc-processor:latest
docker push sonatanfv/vnf-cc-mqttexporter:latest
docker push sonatanfv/vnf-cc-database:latest
docker push sonatanfv/vnf-eae:latest
docker push sonatanfv/vnf-ids-suricata:latest
docker push sonatanfv/vnf-ids-filebeat:latest
docker push sonatanfv/vnf-ids-logstash:latest
docker push sonatanfv/vnf-ids-http:latest
docker push sonatanfv/vnf-ids-elasticsearch:latest
docker push sonatanfv/vnf-ids-kibana:latest
docker push sonatanfv/vnf-proxyvpn:latest

# FSMs
docker push sonatanfv/tng-fsm-industry-pilot-mdc-vnf1:latest
# SSMs
docker push sonatanfv/tng-ssm-industry-pilot-ns2:latest

# SMP-CCS
docker push sonatanfv/smp-ccs:latest
