#!/bin/bash

set -e
docker build -t sonatanfv/vnf-dt:latest -f dt-digitaltwin-docker/containers/Dockerfile dt-digitaltwin-docker/containers/
