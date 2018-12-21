# Edge analytics engine (EAE)

This folder contains the code/Dockerfile in case of Docker-based VNFs.

The EAE will leverage the existing Grafana Docker container to provide a nice visualization of the machine data inside the Prometheus DB.

## Setup

Build from `vnfs` folder:

```bash
docker build -t sonatanfv/vnf-eae:vimemu -f eae-edgeanalyticsengine-emulator/containers/Dockerfile eae-edgeanalyticsengine-emulator/containers/
```

## Usage

Start container:

```bash
docker run -d -p 3000:3000 --rm --name vnf-eae sonatanfv/vnf-eae:vimemu 
# check container is running
docker ps
```

Visit Grafana GUI at `<docker-host>:3000`. On Linux `localhost` and on Windows typically `192.168.99.100`. Login with admin/admin.

### Stop

```bash
docker stop vnf-eae
```

