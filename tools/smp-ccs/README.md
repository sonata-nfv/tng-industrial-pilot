# SMP-CCS


## Local testing

You need two (or more) terminals:

```sh
# Terminal 1: SMP-CC server
smpccs

# Terminal 2: SMP-CC test client (faking the FSM connecting to the server)
smpccc fsm01

# Terminal 3: Additional SMP-CC test clients to test multi-FSM case
smpccc fsm02

# Terminal 4: Do REST requests to API
curl -X GET 127.0.0.1:9011/api/v1/ssmstatus
```

## REST API

### `GET /api/v1/ssmstatus`

Gets a dictionary with the states of all registered SSMs.

Example: 

```sh
curl -X GET 127.0.0.1:9011/api/v1/ssmstatus
```

Returns (Status 200):
```json
{
    "ssm01": {
        "uuid": "ssm01",
        "status": "undefined",
        "created": 1570696345,
        "updated": 1570696345,
        "changed": false,
        "quarantaine": false
    }
}
```

### `PUT /api/v1/ssmstatus`

Updates the state of a registered SSM.
Fields to send:

- `uuid`
- `quarantaine`

Example:

```sh
curl -X PUT 127.0.0.1:9011/api/v1/ssmstatus -d uuid=ssm01 -d quarantaine=1
```

Returns (Status 200):
```
OK
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
