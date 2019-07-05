#!/bin/bash
set -e
source venv_sdk/bin/activate
which tng-project
which tng-validate
which tng-package
BASE_DIR="$(pwd)"
cd sdk-projects/
# trigger service package scripts
echo "Packaging services and VNFs ..."
./pack.sh
cd $BASE_DIR

# trigger test package scripts
echo "Packaging V&V tests ..."
cd vnv-tests/test-packages/
./pack.sh
cd $BASE_DIR