#!/bin/bash
set -e
docker push sonatanfv/vnf-dt:vimemu
docker push sonatanfv/vnf-mdc:vimemu
docker push sonatanfv/vnf-rtr-nat:vimemu
docker push sonatanfv/vnf-cc-broker:vimemu
docker push sonatanfv/vnf-cc-processor:vimemu
docker push sonatanfv/vnf-cc-pushgateway:vimemu
docker push sonatanfv/vnf-cc-database:vimemu
docker push sonatanfv/vnf-eae:vimemu

docker push sonatanfv/vnf-dt:k8s
docker push sonatanfv/vnf-mdc:k8s
docker push sonatanfv/vnf-rtr-nat:k8s
docker push sonatanfv/vnf-cc-broker:k8s
docker push sonatanfv/vnf-cc-processor:k8s
docker push sonatanfv/vnf-eae:k8s