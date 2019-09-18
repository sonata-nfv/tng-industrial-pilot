#!/bin/bash
python -m grpc_tools.protoc --proto_path=. --python_out=src --grpc_python_out=src smpccs.proto