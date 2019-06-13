# tng-industrial-pilot
5GTANGO industrial pilot repository. This pilot is based on a smart manufacturing scenario and contains three use cases:

1. Initial deployment of new machines in a softwarized factory network
2. Intrusion detection and automated intrusion mitigation
3. AR-based maintenance

## Demonstrations

There are several demos developed that show various aspects of this pilot. The demos are categorized in demos running on the [vim-emu](https://osm.etsi.org/wikipub/index.php/VIM_emulator) platform (part of the 5GTANGO SDK) and demos running on Kubernetes (K8s) some of which are controlled by the 5GTANGO service platform.

* vim-emu
    * [IEEE NetSoft 2019: "Prototyping and Demonstrating 5G Verticals: The Smart Manufacturing Case"](https://github.com/sonata-nfv/tng-industrial-pilot/wiki/Demo-NetSoft2019-vim-emu)
* K8s:
    * [Manual deployment on Kubernetes](https://github.com/sonata-nfv/tng-industrial-pilot/wiki/Manual-kubernetes-demo)
    * [Kubernetes deployment with the service platform](https://github.com/sonata-nfv/tng-industrial-pilot/wiki/SP-kubernetes-demo)


## Folder structure

| Folder | Comment |
| --- | --- |
| `doc` | documentation, figures |
| `pipeline` | Scripts for Jenkins CI/CD |
| `sdk-projects` | 5GTANG SDK network service projects (descriptors) |
| `son-sm`| reference to son-sm library to build SSMs and FSMs |
| `ssm` | Service specific managers (SSMs) |
| `vnfs` | All our VNFs and their FSMs |

## CI/CD integration

This repository is connected to a [Jenkins job](https://jenkins.sonata-nfv.eu/view/PIPELINE/job/tng-industrial-pilot/), which automatically builds and publishes the VNFs as well as SDK projects.

* VNFs are outomatically published on DockerHub: [sonatanfv at DockerHub.com](https://hub.docker.com/u/sonatanfv)
* 5GTANGO packages are available in Jenkins: [tng-industrial-pilot/job/master/](https://jenkins.sonata-nfv.eu/view/PIPELINE/job/tng-industrial-pilot/job/master/)

## How to (manually) create 5GTANGO packages

5GTANGO packages can be created from the `sdk-projects` as described in the [README.md](sdk-projects/).

## How to (manually) build the VNFs for this pilot?

Docker images of the VNFs (for various target platforms vim-emu/K8s) used in this pilot can be created in `vnfs/` as described [README.md](vnfs/).
