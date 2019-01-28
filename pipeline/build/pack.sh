#!/bin/bash
BASE_DIR="$(pwd)"
cd sdk-projects/
# trigger VNF build script
./pack.sh
cd $BASE_DIR