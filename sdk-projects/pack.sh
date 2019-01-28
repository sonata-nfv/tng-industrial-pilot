#!/bin/bash
set -e
tng-validate --project tng-smpilot-ns1-emulator -i
tng-validate --project tng-smpilot-ns2-emulator -i
tng-validate --project tng-smpilot-ns1-k8s -i
# package all projects for pilot
tng-pkg -p tng-smpilot-ns1-emulator
tng-pkg -p tng-smpilot-ns2-emulator
tng-pkg -p tng-smpilot-ns1-k8s