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
