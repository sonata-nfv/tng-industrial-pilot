#!/bin/bash
# Script to build all VNFs used for the emulator demo
set -e
target_repo=${1-sonatanfv}

# RTR
docker build -t $target_repo/rtr-nat-ubuntu-emulator -f rtr-nat-ubuntu-emulator/containers/Dockerfile rtr-nat-ubuntu-emulator/containers/

# MDC
docker build -t $target_repo/mdc-machinedatacollector-emulator -f mdc-machinedatacollector-emulator/containers/Dockerfile mdc-machinedatacollector-emulator/containers/
