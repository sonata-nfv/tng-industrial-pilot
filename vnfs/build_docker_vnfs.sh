#!/bin/bash
# Script to build all VNFs used for the emulator demo
set -e
target_repo=${1-sonatanfv}

#
# VNFs for vim-emu
#
# RTR
docker build -t $target_repo/vnf-rtr-nat:vimemu -f rtr-nat-ubuntu-docker/containers/Dockerfile.vimemu rtr-nat-ubuntu-docker/containers/
# CC-CDU01: broker
docker build -t $target_repo/vnf-cc-broker:vimemu -f cc-cloudconnector-docker/containers/cdu_broker/Dockerfile.vimemu cc-cloudconnector-docker/containers/cdu_broker/
# CC-CDU02: processor
docker build -t $target_repo/vnf-cc-processor:vimemu -f cc-cloudconnector-docker/containers/cdu_processor/Dockerfile.vimemu cc-cloudconnector-docker/containers/cdu_processor/
# MDC
docker build -t $target_repo/vnf-mdc:vimemu -f mdc-machinedatacollector-docker/containers/Dockerfile.vimemu mdc-machinedatacollector-docker/containers/
# DT
docker build -t $target_repo/vnf-dt:vimemu -f dt-digitaltwin-docker/containers/Dockerfile.vimemu dt-digitaltwin-docker/containers/
# EAE
docker build -t $target_repo/vnf-eae:vimemu -f eae-edgeanalyticsengine-docker/containers/Dockerfile.vimemu eae-edgeanalyticsengine-docker/containers/

#
# VNFs for Kubernets
#
# TODO