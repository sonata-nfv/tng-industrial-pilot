# Edge analytics engine (EAE)

This folder contains the code/Dockerfile in case of Docker-based VNFs.

The EAE will leverage the existing Grafana Docker container to provide a nice visualization of the machine data, which is temporarily stored inside the CC's Prometheus DB.

## Setup

Here, focus on `:k8s` images. Should work similarly for `:vimemu`-tagged images. 

From `vnfs` folder:

### Build and start CC Prometheus DB

```bash
# build Prometheus CDU
docker build -t sonatanfv/vnf-cc-database:k8s -f cc-cloudconnector-docker/containers/cdu_database/Dockerfile cc-cloudconnector-docker/containers/cdu_database/

# start
docker run -d -p 9090:9090 --rm --name vnf-cc-database sonatanfv/vnf-cc-database:k8s
```

The Prometheus dashboard should now be available at `<docker-host>:9090` (typically `localhost`).

###Build EAE

Build from `vnfs` folder:

```bash
docker build -t sonatanfv/vnf-eae:k8s -f eae-edgeanalyticsengine-docker/containers/Dockerfile eae-edgeanalyticsengine-docker/containers/
```

## Usage

Start container:

```bash
docker run -d -p 3000:3000 --rm --name vnf-eae sonatanfv/vnf-eae:k8s
```

Visit Grafana GUI at `<docker-host>:3000`. On Linux `localhost` and on Windows typically `192.168.99.100`. Login with admin/admin. Login with `admin`/`tango`.

### Stop

```bash
docker stop vnf-eae
docker stop vnf-cc-database
```

