#!/bin/bash
#
# We need the 5GTANGO SDK tools to package the projects.
# uninstall SDK if present (to ensure we have the latest version)
rm -rf venv_sdk
set -e
virtualenv -p /usr/bin/python3 venv_sdk
source venv_sdk/bin/activate
pip3 install --upgrade git+https://github.com/sonata-nfv/tng-sdk-project.git
pip3 install --upgrade git+https://github.com/sonata-nfv/tng-sdk-validation.git
pip3 install --upgrade git+https://github.com/sonata-nfv/tng-sdk-package

tng-project -h
tng-validate -h
tng-package -h
which tng-project
which tng-validate
which tng-package
