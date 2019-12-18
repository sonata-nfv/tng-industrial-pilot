#!/bin/bash

# see http://www.dest-unreach.org/socat/doc/socat-tun.html
echo "Starting socat server..."
socat -d -d TCP-LISTEN:11443,reuseaddr TUN:192.168.255.1/24,up 
