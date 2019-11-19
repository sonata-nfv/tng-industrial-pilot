This is the ns2-ssm specific manager.

# Customise

Edit file at /ns2-ssm/ns2/ns2.py

# Build

```
docker build -t <container_name> -f ns2-ssm/Dockerfile .
```

# Run locally (without external connections)

```sh
# run the container
docker run --rm -it sonatanfv/tng-ssm-industry-pilot-ns2:latest /bin/bash

# test the gRPC SMP-CC client
smpccc
```


#  Test locally using `tng-sdk-sm`

```sh
# use local test SMP-CC
export smpcc_grpc_endpoint=127.0.0.1:9012
# use remote address of SMP-CC
export smpcc_grpc_endpoint=fgcn-tango-smp-ctrl.cs.upb.de:9012
# test configure/initialisation 
tng-sm execute -s ns2-ssm -e configure -p configure_event_initialisation.yml
# test configure/reconfiguration
tng-sm execute -s ns2-ssm -e configure -p configure_event_reconfiguration.yml
```