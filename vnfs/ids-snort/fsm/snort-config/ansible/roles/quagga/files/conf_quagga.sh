#!/bin/bash
red0=$(/sbin/ip route list | grep "dev ens3" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
red1=$(/sbin/ip route list | grep "dev eth1" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
red2=$(/sbin/ip route list | grep "dev eth2" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
red3=$(/sbin/ip route list | grep "dev eth3" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
red4=$(/sbin/ip route list | grep "dev eth4" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
echo $red0;
mask0=$(/sbin/ip route list | grep "dev ens3" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
mask1=$(/sbin/ip route list | grep "dev eth1" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
mask2=$(/sbin/ip route list | grep "dev eth2" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
mask3=$(/sbin/ip route list | grep "dev eth3" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
mask4=$(/sbin/ip route list | grep "dev eth4" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
echo $mask0;
ip0=$(/sbin/ifconfig ens3 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
ip1=$(/sbin/ifconfig eth1 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
ip2=$(/sbin/ifconfig eth2 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
ip3=$(/sbin/ifconfig eth3 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
ip4=$(/sbin/ifconfig eth4 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
echo $ip0;
bash <<EOF2
cat >> /tmp/teste << EOF
interface eth0
interface eth1
interface eth2
interface eth3
interface eth4
interface lo
router ospf
 passive-interface eth1
EOF
echo " network $red0/$mask0 area 0.0.0.0" >> /tmp/teste
echo " network $red1/$mask1 area 0.0.0.0" >> /tmp/teste
echo " network $red2/$mask2 area 0.0.0.0" >> /tmp/teste
echo " network $red3/$mask3 area 0.0.0.0" >> /tmp/teste
echo " network $red4/$mask4 area 0.0.0.0" >> /tmp/teste
echo "line vty" >> /tmp/teste
EOF
echo "interface eth0" >> /tmp/teste2
echo " ip address $ip0/$mask0" >> /tmp/teste2
cat >> /tmp/teste2 << EOF
 ipv6 nd suppress-ra
interface enp0s9
 ip address 192.168.100.1/24
 ipv6 nd suppress-ra
interface enp0s10
 ip address 192.168.101.2/24
 ipv6 nd suppress-ra
interface lo
ip forwarding
line vty
EOF
echo "Finished"
exit
EOF2






bash <<EOF2
apt-get update
apt-get install quagga quagga-doc traceroute
cp /usr/share/doc/quagga/examples/zebra.conf.sample /etc/quagga/zebra.conf
cp /usr/share/doc/quagga/examples/ospfd.conf.sample /etc/quagga/ospfd.conf
chown quagga.quaggavty /etc/quagga/*.conf
chmod 640 /etc/quagga/*.conf
sed -i s'/zebra=no/zebra=yes/' /etc/quagga/daemons
sed -i s'/ospfd=no/ospfd=yes/' /etc/quagga/daemons
echo 'VTYSH_PAGER=more' >>/etc/environment 
echo 'export VTYSH_PAGER=more' >>/etc/bash.bashrc
cat >> /etc/quagga/ospfd.conf << EOF
interface eth0
interface eth1
interface eth2
interface eth3
interface eth4
interface lo
router ospf
 passive-interface eth1
 network 192.168.1.0/24 area 0.0.0.0
 network 192.168.100.0/24 area 0.0.0.0
 network 192.168.101.0/24 area 0.0.0.0
line vty
EOF
cat >> /etc/quagga/zebra.conf << EOF
interface eth0
interface enp0s8
 ip address 192.168.1.254/24
 ipv6 nd suppress-ra
interface enp0s9
 ip address 192.168.100.1/24
 ipv6 nd suppress-ra
interface enp0s10
 ip address 192.168.101.2/24
 ipv6 nd suppress-ra
interface lo
ip forwarding
line vty
EOF
/etc/init.d/quagga start
exit
EOF2
