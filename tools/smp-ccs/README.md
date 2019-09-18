# SMP-CCS


## Local testing

You need two terminals:

```sh
# Terminal 1: SMP-CC server
smpccs

# Terminal 2: SMP-CC test client (faking the FSM connecting to the server)
smpccc

```

## gRPC: How to and documentation

* see this [tutorial](https://grpc.io/docs/tutorials/basic/python/)

Requires:

```
pip install grpcio-tools
```

Generate client and server code:

```
python -m grpc_tools.protoc --proto_path=src/smpccs/ --python_out=src/smpccs/ --grpc_python_out=src/smpccs src/smpccs/smpccs.proto            
```

Also see `./gen_proto.sh`.
