#!/bin/bash
# Script to build all VNFs used for the emulator demo
set -e
target_repo=${1-sonatanfv}

#
# VNFs for Kubernets
# tag with :k8s and :latest to ensure auto updates by kubernetes
#
# usecase3
docker build -t $target_repo/vnf-proxyvpn:k8s -t $target_repo/vnf-proxyvpn:latest -f usecase3/containers/proxyvpn/Dockerfile usecase3/containers/proxyvpn
