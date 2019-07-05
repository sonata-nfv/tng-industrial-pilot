# VNFs for Industry Pilot

## Build all with:

```sh
./build_docker_vnfs.sh
```

## Versions

Each VNF can have **multiple Dockerfiles** because we need multiple images for different target environments, i.e., [vim-emu](https://github.com/sonata-nfv/son-emu/wiki/Container-Requirements) vs. Kubernets:


1. `Dockerfile`: Generates image for K8s deployment (tagged `:k8s`)
1. `Dockerfile.vimemu`: Generates image for K8s deployment (tagged `:vimemu`)


The result of a build should look like this:

```sh
$ docker images

REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
sonatanfv/vnf-eae            k8s                 91a4a50270f1        5 minutes ago       240MB
sonatanfv/vnf-eae            vimemu              91a4a50270f1        5 minutes ago       240MB
sonatanfv/vnf-dt             k8s                 20e49539ad8a        5 minutes ago       876MB
sonatanfv/vnf-dt             vimemu              20e49539ad8a        5 minutes ago       876MB
sonatanfv/vnf-mdc            k8s                 2eb02cc2708b        8 minutes ago       582MB
sonatanfv/vnf-mdc            vimemu              2eb02cc2708b        8 minutes ago       582MB
sonatanfv/vnf-cc-processor   k8s                 2792c86a1b03        9 minutes ago       680MB
sonatanfv/vnf-cc-processor   vimemu              2792c86a1b03        9 minutes ago       680MB
sonatanfv/vnf-cc-broker      k8s                 394af3eba255        11 minutes ago      261MB
sonatanfv/vnf-cc-broker      vimemu              394af3eba255        11 minutes ago      261MB
sonatanfv/vnf-rtr-nat        k8s                 28a5cc1d2034        12 minutes ago      150MB
sonatanfv/vnf-rtr-nat        vimemu              28a5cc1d2034        12 minutes ago      150MB
```