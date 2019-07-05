#!/bin/bash
set -e
# directly call the validator (to make error pasing simple)
tng-validate --project TSTINDP -t

# package all projects
tng-pkg -p TSTINDP --skip-validation
