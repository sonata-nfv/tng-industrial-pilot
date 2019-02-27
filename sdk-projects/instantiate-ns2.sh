#!/bin/bash
sudo curl -X GET http://127.0.0.1:5000/instantiations
curl -X POST http://127.0.0.1:5000/instantiations -d '{"service_name": "tng-smpilot-ns2-emulator"}'
sudo ovs-vsctl set port dc2.s1-eth4 tag=1



