#!/bin/bash
set -e
source venv_sdk/bin/activate
which tng-project
which tng-validate
which tng-package
BASE_DIR="$(pwd)"
cd sdk-projects/
# trigger service package scripts
./pack.sh
cd $BASE_DIR

# trigger test package scripts
cd vnv-tests/test-packages/
./pack.sh
cd $BASE_DIR