#!/bin/bash
# Script to build all VNFs used for the emulator demo
set -e
target_repo=${1-sonatanfv}

# RTR
docker build -t $target_repo/vnf-rtr-nat:vimemu -f rtr-nat-ubuntu-emulator/containers/Dockerfile rtr-nat-ubuntu-emulator/containers/

# CC-CDU01: broker
docker build -t $target_repo/vnf-cc-broker:vimemu -f cc-cloudconnector-emulator/containers/cdu_broker/Dockerfile cc-cloudconnector-emulator/containers/cdu_broker/

# CC-CDU02: processor
docker build -t $target_repo/vnf-cc-processor:vimemu -f cc-cloudconnector-emulator/containers/cdu_processor/Dockerfile cc-cloudconnector-emulator/containers/cdu_processor/

# MDC
docker build -t $target_repo/vnf-mdc:vimemu -f mdc-machinedatacollector-emulator/containers/Dockerfile mdc-machinedatacollector-emulator/containers/

# DT
docker build -t $target_repo/vnf-dt:vimemu -f dt-digitaltwin-emulator/containers/Dockerfile dt-digitaltwin-emulator/containers/

# EAE
docker build -t $target_repo/vnf-eae:vimemu -f eae-edgeanalyticsengine-emulator/containers/Dockerfile eae-edgeanalyticsengine-emulator/containers/
