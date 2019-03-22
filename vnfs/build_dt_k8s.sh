#!/bin/bash

set -e
docker build -t sonatanfv/vnf-dt:k8s -f dt-digitaltwin-docker/containers/Dockerfile dt-digitaltwin-docker/containers/
