#!/bin/bash
set -e
# directly call the validator to have different validation levels for different projects
tng-validate --project tng-smpilot-ns3-k8s -i
# package all projects for pilot (we skip the validation, because we did it already by directly calling the validator)
tng-pkg -p tng-smpilot-ns3-k8s --skip-validation
