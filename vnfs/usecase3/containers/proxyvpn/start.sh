#!/bin/bash
openvpn --config /etc/openvpn/client3.ovpn &
squid -N -f /etc/squid/squid.conf -z &
squid -f /etc/squid/squid.conf -NYCd 1

