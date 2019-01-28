# VNFs for Industry Pilot

## Build all with:

```sh
./build_docker_vnfs.sh
```

## Versions

Each VNF can have **multiple Dockerfiles** because we need multiple images for different target environments, i.e., [vim-emu](https://github.com/sonata-nfv/son-emu/wiki/Container-Requirements) vs. Kubernets:


1. `Dockerfile`: Generates image for K8s deployment (tagged `:k8s`)
1. `Dockerfile.vimemu`: Generates image for K8s deployment (tagged `:vimemu`)