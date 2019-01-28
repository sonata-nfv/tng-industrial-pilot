#!/bin/bash
set -e
# package all projects for pilot
tng-pkg -p tng-smpilot-ns1-emulator -v
tng-pkg -p tng-smpilot-ns2-emulator -v
tng-pkg -p tng-smpilot-ns1-k8s -v