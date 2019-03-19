#!/bin/bash
# Script to build all VNFs used for the emulator demo
set -e
target_repo=${1-sonatanfv}

#
# VNFs for Kubernets
#
# RTR
docker build -t $target_repo/vnf-rtr-nat:k8s -f rtr-nat-ubuntu-docker/containers/Dockerfile rtr-nat-ubuntu-docker/containers/
# CC-CDU01: broker
docker build -t $target_repo/vnf-cc-broker:k8s -f cc-cloudconnector-docker/containers/cdu_broker/Dockerfile cc-cloudconnector-docker/containers/cdu_broker/
# CC-CDU02: processor
docker build -t $target_repo/vnf-cc-processor:k8s -f cc-cloudconnector-docker/containers/cdu_processor/Dockerfile cc-cloudconnector-docker/containers/cdu_processor/
# CC-CDU03: mqtt exporter
docker build -t $target_repo/vnf-cc-mqttexporter:k8s -f cc-cloudconnector-docker/containers/cdu_mqttexporter/Dockerfile cc-cloudconnector-docker/containers/cdu_mqttexporter/
# CC-CDU04: database
docker build -t $target_repo/vnf-cc-database:k8s -f cc-cloudconnector-docker/containers/cdu_database/Dockerfile cc-cloudconnector-docker/containers/cdu_database/
# MDC
docker build -t $target_repo/vnf-mdc:k8s -f mdc-machinedatacollector-docker/containers/Dockerfile mdc-machinedatacollector-docker/containers/
# DT
docker build -t $target_repo/vnf-dt:k8s -f dt-digitaltwin-docker/containers/Dockerfile dt-digitaltwin-docker/containers/
# EAE
docker build -t $target_repo/vnf-eae:k8s -f eae-edgeanalyticsengine-docker/containers/Dockerfile eae-edgeanalyticsengine-docker/containers/

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