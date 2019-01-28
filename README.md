# tng-industrial-pilot
5GTANGO industrial pilot repository


## Folder structure

| Folder | Comment |
| --- | --- |
| `doc` | documentation, figures |
| `sdk-projects` | 5GTANG SDK network service projects (descriptors) |
| `son-sm`| reference to son-sm library to build SSMs and FSMs |
| `ssm` | Service specific managers (SSMs) |
| `vnfs` | All our VNFs and their FSMs |

## How to create 5GTANGO packages

5GTANGO packages can be created from the `sdk-projects` as described in the [README.md](sdk-projects/).

## How to build the VNFs for this pilot?

Docker images of the VNFs (for various target platforms vim-emu/K8s) used in this pilot can be created in `vnfs/` as described [README.md](vnfs/).
