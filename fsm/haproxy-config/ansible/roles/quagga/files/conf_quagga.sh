#!/bin/bash
red0=$(/sbin/ip route list | grep "dev eth0" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
red1=$(/sbin/ip route list | grep "dev eth1" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
red2=$(/sbin/ip route list | grep "dev eth2" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
red3=$(/sbin/ip route list | grep "dev eth3" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
red4=$(/sbin/ip route list | grep "dev eth4" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 1);
mask0=$(/sbin/ip route list | grep "dev eth0" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
mask1=$(/sbin/ip route list | grep "dev eth1" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
mask2=$(/sbin/ip route list | grep "dev eth2" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
mask3=$(/sbin/ip route list | grep "dev eth3" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
mask4=$(/sbin/ip route list | grep "dev eth4" | awk '{printf "%s\n", $1 }' | grep '/' | cut -d / -f 2);
ip0=$(/sbin/ifconfig eth0 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
ip1=$(/sbin/ifconfig eth1 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
ip2=$(/sbin/ifconfig eth2 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
ip3=$(/sbin/ifconfig eth3 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
ip4=$(/sbin/ifconfig eth4 | grep "inet " | awk '{ printf "%s", $2 }' | cut -d : -f 2);
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
EOF
echo " network $red0/$mask0 area 0.0.0.0" >> /etc/quagga/ospfd.conf
echo " network $red1/$mask1 area 0.0.0.0" >> /etc/quagga/ospfd.conf
echo " network $red2/$mask2 area 0.0.0.0" >> /etc/quagga/ospfd.conf
echo " network $red3/$mask3 area 0.0.0.0" >> /etc/quagga/ospfd.conf
echo " network $red4/$mask4 area 0.0.0.0" >> /etc/quagga/ospfd.conf
echo "line vty" >> /etc/quagga/ospfd.conf
echo "interface eth0" >> /etc/quagga/zebra.conf
echo " ip address $ip0/$mask0" >> /etc/quagga/zebra.conf
echo " ipv6 nd suppress-ra" >> /etc/quagga/zebra.conf
echo "interface eth1" >> /etc/quagga/zebra.conf
echo " ip address $ip1/$mask1" >> /etc/quagga/zebra.conf
echo " ipv6 nd suppress-ra" >> /etc/quagga/zebra.conf
echo "interface eth2" >> /etc/quagga/zebra.conf
echo " ip address $ip2/$mask2" >> /etc/quagga/zebra.conf
echo " ipv6 nd suppress-ra" >> /etc/quagga/zebra.conf
echo "interface eth3" >> /etc/quagga/zebra.conf
echo " ip address $ip3/$mask3" >> /etc/quagga/zebra.conf
echo " ipv6 nd suppress-ra" >> /etc/quagga/zebra.conf
echo "interface eth4" >> /etc/quagga/zebra.conf
echo " ip address $ip4/$mask4" >> /etc/quagga/zebra.conf
echo " ipv6 nd suppress-ra" >> /etc/quagga/zebra.conf
cat >> /etc/quagga/zebra.conf << EOF
interface lo
ip forwarding
line vty
EOF
/etc/init.d/quagga start
exit
EOF2
