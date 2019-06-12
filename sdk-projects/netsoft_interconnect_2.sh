#!/bin/bash
# NS2.3 -> NS1.2
sudo ovs-vsctl set port dc1.s1-eth9 tag=6
# NS2.4 -> NS1.2
sudo ovs-vsctl set port dc4.s1-eth3 tag=6
