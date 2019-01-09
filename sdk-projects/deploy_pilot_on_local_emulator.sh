#!/bin/bash
sudo ls *.tgo

curl -i -X POST -F package=@eu.5gtango.tng-smpilot-ns1-emulator.0.1.tgo http://127.0.0.1:5000/packages
sleep 1
curl -i -X POST -F package=@eu.5gtango.tng-smpilot-ns2-emulator.0.1.tgo http://127.0.0.1:5000/packages
sleep 1
curl -X POST http://127.0.0.1:5000/instantiations -d '{"service_name": "tng-smpilot-ns1-emulator"}'
sleep 1
curl -X POST http://127.0.0.1:5000/instantiations -d '{"service_name": "tng-smpilot-ns2-emulator"}'

sudo ovs-vsctl set port dc2.s1-eth6 tag=2



