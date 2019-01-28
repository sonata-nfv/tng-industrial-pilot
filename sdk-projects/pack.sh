#!/bin/bash
set -e
tng-validate --project tng-smpilot-ns1-emulator -i
tng-validate --project tng-smpilot-ns2-emulator -s # we cannot do syntax here because of additional address fields for emulator
tng-validate --project tng-smpilot-ns1-k8s -s # -i still buggy
# package all projects for pilot
tng-pkg -p tng-smpilot-ns1-emulator
tng-pkg -p tng-smpilot-ns2-emulator
tng-pkg -p tng-smpilot-ns1-k8s