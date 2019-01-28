#!/bin/bash
#
# We need the 5GTANGO SDK tools to package the projects.
pip3 install git+https://github.com/sonata-nfv/tng-sdk-project.git
pip3 install git+https://github.com/sonata-nfv/tng-sdk-validation.git
pip3 install git+https://github.com/sonata-nfv/tng-sdk-package

tng-project -h
tng-validate -h
tng-package -h