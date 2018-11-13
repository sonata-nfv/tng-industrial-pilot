# tng-industrial-pilot
5GTANGO industrial pilot repository


## Folder structure

| --- | --- |
| `doc` | documentation, figures |
| `sdk-projects` | 5GTANG SDK network service projects (descriptors) |
| `son-sm`| reference to son-sm library to build SSMs and FSMs |
| `ssm` | Service specific managers (SSMs) |
| `vnfs` | All our VNFs and their FSMs |
| `vnfs/(vnf_name)/vnf_source` | Source, Dockerfile of VNFs as such (in case of Docker-based VNFs) |
| `vnfs/(vnf_name)/fsm` | FSMs: code, Dockerfile etc. |

