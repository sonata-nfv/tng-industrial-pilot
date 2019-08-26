#!/bin/bash
set -e
BASE_DIR="$(pwd)"

# VNFs
cd vnfs/
# trigger VNF build script
./build_docker_vnfs.sh
cd $BASE_DIR

# FSMs
cd fsms/
# trigger VNF build script
./build.sh
cd $BASE_DIR