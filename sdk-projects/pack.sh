#!/bin/bash
set -e
# package all projects for pilot
tng-validate -s --project tng-smpilot-ns1-emulator/  # sytax validation only (as long as we have to skip integrety validation for CNFs)
tng-pkg -p tng-smpilot-ns1-emulator  --skip-validation  # skip integrety validation until validator supports CNFs