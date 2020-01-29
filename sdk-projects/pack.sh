#!/bin/bash
set -e
# directly call the validator to have different validation levels for different projects
#tng-validate --project tng-smpilot-ns1-emulator -i
#tng-validate --project tng-smpilot-ns2-emulator -i
tng-validate --project tng-smpilot-ns1-k8s -s
#tng-validate --project tng-smpilot-ns2-k8s -s
tng-validate --project tng-smpilot-ns2-k8s-eids -s
tng-validate --project tng-smpilot-ns3-k8s -i
# package all projects for pilot (we skip the validation, because we did it already by directly calling the validator)
#tng-pkg -p tng-smpilot-ns1-emulator --skip-validation
#tng-pkg -p tng-smpilot-ns2-emulator --skip-validation
tng-pkg -p tng-smpilot-ns1-k8s --skip-validation
#tng-pkg -p tng-smpilot-ns2-k8s --skip-validation
tng-pkg -p tng-smpilot-ns2-k8s-eids --skip-validation
tng-pkg -p tng-smpilot-ns3-k8s --skip-validation