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
# trigger FSM build script
./build.sh
cd $BASE_DIR

# SSMs
cd ssms/
# trigger SSM build script
./build.sh
cd $BASE_DIR

# SMP-CCS
cd tools/smp-ccs/
# trigger build script
./build.sh
cd $BASE_DIR