#!/bin/bash
# Script to build all VNFs used for the emulator demo
set -e
target_repo=${1-sonatanfv}

#
# VNFs for Kubernets
# tag with :k8s and :latest to ensure auto updates by kubernetes
#
# CC-CDU01: broker
docker build -t $target_repo/vnf-cc-broker:k8s -t $target_repo/vnf-cc-broker:latest -f cc-cloudconnector-docker/containers/cdu_broker/Dockerfile cc-cloudconnector-docker/containers/cdu_broker/
# CC-CDU02: processor
docker build -t $target_repo/vnf-cc-processor:k8s -t $target_repo/vnf-cc-processor:latest -f cc-cloudconnector-docker/containers/cdu_processor/Dockerfile cc-cloudconnector-docker/containers/cdu_processor/
# CC-CDU03: mqtt exporter
docker build -t $target_repo/vnf-cc-mqttexporter:k8s -t $target_repo/vnf-cc-mqttexporter:latest -f cc-cloudconnector-docker/containers/cdu_mqttexporter/Dockerfile cc-cloudconnector-docker/containers/cdu_mqttexporter/
# CC-CDU04: database
docker build -t $target_repo/vnf-cc-database:k8s -t $target_repo/vnf-cc-database:latest -f cc-cloudconnector-docker/containers/cdu_database/Dockerfile cc-cloudconnector-docker/containers/cdu_database/
# MDC
docker build -t $target_repo/vnf-mdc:k8s -t $target_repo/vnf-mdc:latest -f mdc-machinedatacollector-docker/containers/Dockerfile mdc-machinedatacollector-docker/containers/
# DT
docker build -t $target_repo/vnf-dt:k8s -t $target_repo/vnf-dt:latest -f dt-digitaltwin-docker/containers/Dockerfile dt-digitaltwin-docker/containers/
# EAE
docker build -t $target_repo/vnf-eae:k8s -t $target_repo/vnf-eae:latest -f eae-edgeanalyticsengine-docker/containers/Dockerfile eae-edgeanalyticsengine-docker/containers/
### IDS VNFs
# s: suricata
docker build -t $target_repo/vnf-ids-suricata:k8s -t $target_repo/vnf-ids-suricata:latest -f ids-selk/s/Dockerfile ids-selk/s/
# f: filebeat
docker build -t $target_repo/vnf-ids-filebeat:k8s -t $target_repo/vnf-ids-filebeat:latest -f ids-selk/f/Dockerfile ids-selk/f/
# l: logstash
docker build -t $target_repo/vnf-ids-logstash:k8s -t $target_repo/vnf-ids-logstash:latest -f ids-selk/l/Dockerfile ids-selk/l/
# h: http server
docker build -t $target_repo/vnf-ids-http:k8s -t $target_repo/vnf-ids-http:latest -f ids-selk/h/Dockerfile ids-selk/h/
# e: elasticsearch
docker build -t $target_repo/vnf-ids-elasticsearch:k8s -t $target_repo/vnf-ids-elasticsearch:latest -f ids-selk/e/Dockerfile ids-selk/e/
# k: kibana
docker build -t $target_repo/vnf-ids-kibana:k8s -t $target_repo/vnf-ids-kibana:latest -f ids-selk/k/Dockerfile ids-selk/k/
# usecase3
docker build -t $target_repo/vnf-proxy:k8s -t $target_repo/vnf-proxy:latest -f usecase3/containers/proxy/Dockerfile usecase3/containers/proxy
docker build -t $target_repo/vnf-proxyvpn:k8s -t $target_repo/vnf-proxyvpn:latest -f usecase3/containers/proxyvpn/Dockerfile usecase3/containers/proxyvpn


#
# VNFs for vim-emu
#
# RTR
docker build -t $target_repo/vnf-rtr-nat:vimemu -f rtr-nat-ubuntu-docker/containers/Dockerfile.vimemu rtr-nat-ubuntu-docker/containers/
# CC-CDU01: broker
docker build -t $target_repo/vnf-cc-broker:vimemu -f cc-cloudconnector-docker/containers/cdu_broker/Dockerfile.vimemu cc-cloudconnector-docker/containers/cdu_broker/
# CC-CDU02: processor
docker build -t $target_repo/vnf-cc-processor:vimemu -f cc-cloudconnector-docker/containers/cdu_processor/Dockerfile.vimemu cc-cloudconnector-docker/containers/cdu_processor/
# CC-CDU03: mqtt exporter
docker build -t $target_repo/vnf-cc-mqttexporter:vimemu -f cc-cloudconnector-docker/containers/cdu_mqttexporter/Dockerfile.vimemu cc-cloudconnector-docker/containers/cdu_mqttexporter/
# CC-CDU04: database
docker build -t $target_repo/vnf-cc-database:vimemu -f cc-cloudconnector-docker/containers/cdu_database/Dockerfile.vimemu cc-cloudconnector-docker/containers/cdu_database/
# MDC
docker build -t $target_repo/vnf-mdc:vimemu -f mdc-machinedatacollector-docker/containers/Dockerfile.vimemu mdc-machinedatacollector-docker/containers/
# DT
docker build -t $target_repo/vnf-dt:vimemu -f dt-digitaltwin-docker/containers/Dockerfile.vimemu dt-digitaltwin-docker/containers/
# EAE
docker build -t $target_repo/vnf-eae:vimemu -f eae-edgeanalyticsengine-docker/containers/Dockerfile.vimemu eae-edgeanalyticsengine-docker/containers/
