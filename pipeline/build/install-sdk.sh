#!/bin/bash
#
# We need the 5GTANGO SDK tools to package the projects.
# uninstall SDK if present (to ensure we have the latest version)
sudo pip3 uninstall tngsdk.project
sudo pip3 uninstall tngsdk.validate
sudo pip3 uninstall tngsdk.package
set -e
sudo pip3 install --upgrade git+https://github.com/sonata-nfv/tng-sdk-project.git
sudo pip3 install --upgrade git+https://github.com/sonata-nfv/tng-sdk-validation.git
sudo pip3 install --upgrade git+https://github.com/sonata-nfv/tng-sdk-package

tng-project -h
tng-validate -h
tng-package -h