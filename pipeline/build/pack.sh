#!/bin/bash
set -e
source venv_sdk/bin/activate
BASE_DIR="$(pwd)"
cd sdk-projects/
# trigger VNF build script
./pack.sh
cd $BASE_DIR