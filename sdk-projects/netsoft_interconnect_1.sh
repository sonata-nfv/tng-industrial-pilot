#!/bin/bash
# NS2.0 -> NS1.0
sudo ovs-vsctl set port dc2.s1-eth10 tag=1
# NS2.1 -> NS1.0
sudo ovs-vsctl set port dc3.s1-eth3 tag=1
# NS2.2 -> NS1.1
sudo ovs-vsctl set port dc6.s1-eth3 tag=2
# NS2.3 -> NS1.2
#sudo ovs-vsctl set port dc1.s1-eth9 tag=6
# NS2.4 -> NS1.2
#sudo ovs-vsctl set port dc4.s1-eth3 tag=6
