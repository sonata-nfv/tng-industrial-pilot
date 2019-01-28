#!/bin/bash
BASE_DIR="$(pwd)"
cd vnfs/
# trigger VNF build script
./build_docker_vnfs.sh
cd $BASE_DIR