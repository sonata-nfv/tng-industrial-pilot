# tng-industrial-pilot
5GTANGO industrial pilot repository


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
