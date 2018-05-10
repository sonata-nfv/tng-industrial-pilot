#!/usr/bin/env python3

import os
import logging
import paramiko
import configparser
from abc import ABCMeta, abstractmethod

class Factory:
    def get_os_implementation(self, os, logger):

        if os == "ubuntu":
            return Ubuntu_implementation(logger)
        elif os == "\"centos\"":
            return Centos_implementation(logger)
        else:
            raise NotImplementedError("Unknown OS type.")

class OS_implementation(metaclass = ABCMeta):
    config_dir = './ansible/roles/quagga/files'
    monitoring_file = './node.conf'
    LOG = None

    def __init__(self, logger):
        self.LOG = logger
    
    @abstractmethod
    def configure_interfaces(self, ssh = None):
        raise NotImplementedError("Not implemented")
    
    @abstractmethod
    def configure_quagga_forwarding_rules(self, ssh, gw):
        raise NotImplementedError("Not implemented")

    def configure_monitoring(self, ssh, host_ip):
        ftp = ssh.open_sftp()
        self.LOG.info("SFTP connection established")

        self.createConf(host_ip, 4, 'cache-vnf')
        localpath = self.monitoring_file
        self.LOG.info("SFTP connection entering on %s", localpath)
        remotepath = '/tmp/node.conf'
        sftpa = ftp.put(localpath, remotepath)
        ftp.close()

        self.LOG.info("SSH connection reestablished")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo cp /tmp/node.conf /opt/Monitoring')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl restart mon-probe.service')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))
                
    def stop_service(self, ssh):
        self.LOG.info("SSH connection established")

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl stop quagga')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))
        
    def scale_service(self, ssh):
        self.LOG.info("SSH connection established")

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl start quagga')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

    @abstractmethod
    def reconfigure_service(self, ssh, cfg):
        raise NotImplementedError("Not implemented")
        
    @abstractmethod
    def configure_forward_routing(self, ssh, host_ip, data_ip, next_ip):
        raise NotImplementedError("Not implemented")
    
    def createConf(self, pw_ip, interval, name):

        #config = configparser.RawConfigParser()
        config = configparser.ConfigParser(interpolation = None)
        config.add_section('vm_node')
        config.add_section('Prometheus')
        config.set('vm_node', 'node_name', name)
        config.set('vm_node', 'post_freq', str(interval))
        config.set('Prometheus', 'server_url', 'http://' + pw_ip + ':9091/metrics')
    
    
        with open('node.conf', 'w') as configfile:    # save
            config.write(configfile)
    
        f = open('node.conf', 'r')
        self.LOG.debug('Mon Config-> ' + "\n" + f.read())
        f.close()
    
class Centos_implementation(OS_implementation):
    
    def __init__(self, logger):
        self.LOG = logger
    
    def configure_interfaces(self, ssh):
        self.LOG.info("configure_interfaces centos")
        
        if ssh == None:
            return;
        
        self.LOG.info("Copy net interfaces cfg files")
        ftp = ssh.open_sftp()
        self.LOG.info("SFTP connection established")

        localpath = self.config_dir + '/ifcfg-eth1'
        self.LOG.info("SFTP connection entering on %s", localpath)
        remotepath = '/tmp/ifcfg-eth1'
        sftpa = ftp.put(localpath, remotepath)
        localpath = self.config_dir + '/ifcfg-eth2'
        remotepath = '/tmp/ifcfg-eth2'
        self.LOG.info("SFTP connection entering on %s", localpath)
        sftpa = ftp.put(localpath, remotepath)
        ftp.close()

        self.LOG.info("Making sure the hostname is resolvable")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('echo "127.0.0.1 $(hostname)" | sudo tee -a /etc/hosts')
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Making sure .ssh directory exists")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("[ -d .ssh ] && echo OK")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
        if sout != "OK":
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("mkdir .ssh")
            sout = ssh_stdout.read().decode('utf-8')
            serr = ssh_stderr.read().decode('utf-8')
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("chmod 700 .ssh")
            sout = ssh_stdout.read().decode('utf-8')
            serr = ssh_stderr.read().decode('utf-8')
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Copying scripts")
#        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo cp /tmp/ifcfg-eth1 /etc/sysconfig/network-scripts && sudo cp /tmp/ifcfg-eth2 /etc/sysconfig/network-scripts")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo cp /tmp/ifcfg-eth1 /etc/sysconfig/network-scripts")
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Displaying eth1 data")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/sbin/ifconfig eth1")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

#        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("echo \"HWADDRESS=\"$(/sbin/ifconfig eth2 | awk '/ether/ { print $2 } ') | sudo su -c 'cat >> /etc/sysconfig/network-scripts/ifcfg-eth2'")
#        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
#        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Updating ifcfg-eth1")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("echo \"HWADDRESS=\"$(/sbin/ifconfig eth1 | awk '/ether/ { print $2 } ') | sudo su -c 'cat >> /etc/sysconfig/network-scripts/ifcfg-eth1'")
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Force ip forwarding")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("echo '1' | sudo tee /proc/sys/net/ipv4/ip_forward")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Get eth1 (input) subnetwork")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/usr/sbin/ip route list | grep -m 1 '/27 dev eth1' | awk '{printf \"%s\",$1}'")
        input_subnetwork = ssh_stdout.read().decode('utf-8').strip()
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(input_subnetwork, serr))

        self.LOG.info("Delete extraneous rule on eth2 (output)")
        #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /usr/sbin/ip route del {0} dev eth2".format(input_subnetwork))
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /usr/sbin/ip route del {0} dev eth1".format(input_subnetwork))
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Get current default GW")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/usr/sbin/ip route | awk '/default/ { print $3 }'")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
        return sout.strip()

    def configure_quagga_forwarding_rules(self, ssh, gw):

        self.LOG.info("Always use eth0 (mgmt) for connection to 10.230.x.x for protecting admin ssh connections")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "sudo /usr/sbin/ip route add 10.230.0.0/16 dev eth0 via {0}".format(gw))
        # FIX: how to known that eth0 is always mgmt ?
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))

        self.LOG.info('get own ip')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/sbin/ifconfig eth0 | grep \"inet\" | awk '{ if ($1 == \"inet\") {print $2} }'")
        my_ip = ssh_stdout.read().decode('utf-8').strip()
        self.LOG.info('stdout from remote: ' + my_ip)
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info('Port 80 to 3128 for {0}'.format(my_ip))
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /usr/sbin/iptables -t nat -A PREROUTING -i eth1 -p tcp -m tcp --dport 80 -j DNAT --to-destination '{0}:3128'".format(my_ip))
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Redirecting port")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo /usr/sbin/iptables -t nat -A PREROUTING -i eth1 -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 3128')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Setting masquerade")
        #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo /usr/sbin/iptables -t nat -A POSTROUTING -o eth2 -j MASQUERADE')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo /usr/sbin/iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Accept in the filter table")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo /usr/sbin/iptables -t filter -A INPUT -p tcp --dport 3128 -j ACCEPT')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))
        
        self.LOG.info("Configuration of quagga service")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl start quagga')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

    def reconfigure_service(self, ssh, cfg):
        self.LOG.info("SSH connection established")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl stop quagga')
        self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('output from remote: ' + ssh_stderr.read().decode('utf-8'))
        
        ftp = ssh.open_sftp()
        self.LOG.info("SFTP connection established")

        if cfg == "transparent":
            localpath = self.config_options[cfg]
            self.LOG.info("SFTP connection entering on %s", localpath)
            remotepath = '/tmp/quagga.conf'
            sftpa = ftp.put(localpath, remotepath)
        elif cfg == "squidguard":
            cfg = "squid_ufdb_centos"
            localpath = self.config_options[cfg]
            self.LOG.info("SFTP connection entering on %s", localpath)
            remotepath = '/tmp/quagga.conf'
            sftpa = ftp.put(localpath, remotepath)
            localpath = self.config_options["ufdbguardconf"]
            self.LOG.info("SFTP connection entering on %s", localpath)
            remotepath = '/tmp/ufdbguard.conf'
            sftpa = ftp.put(localpath, remotepath)

        ftp.close()

        self.LOG.info("Moving the Squid configuration file")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo mv /etc/quagga/quagga.conf /etc/quagga/quagga.conf.old')
        self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))
        self.LOG.info("Copying the Squid configuration file")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo cp /tmp/quagga.conf /etc/quagga')
        self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))

        if cfg == "squid_ufdb_centos":
            self.LOG.info("Copying the Squid Guard configuration file")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("[ -f /etc/ufdbguard/ufdbGuard.conf ] && echo OK")
            sout = ssh_stdout.read().decode('utf-8')
            self.LOG.info('output from remote: ' + sout)
            self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))

            if sout == "OK":
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo su -c 'mv /etc/ufdbguard/ufdbGuard.conf /etc/ufdbguard/ufdbGuard.conf.old'") 
                self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
                self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))
            
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo su -c 'mv /tmp/ufdbguard.conf /etc/ufdbguard/ufdbGuard.conf'")
            self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
            self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo systemctl start ufdb.service")
            self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
            self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Restarting Squid")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl restart quagga')
        self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))

    def configure_forward_routing(self, ssh, host_ip, data_ip, next_ip):
        self.LOG.info("Retrieve FSM IP address")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "FSM_IP=$(echo $SSH_CLIENT | awk '{ print $1}') && echo $FSM_IP")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
        fsm_ip = sout.strip()
        self.LOG.info("FSM IP: {0}".format(fsm_ip))

        self.LOG.info("Get current default GW")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("IP=$(/usr/sbin/ip route | awk '/default/ { print $3 }') && echo $IP")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
        default_gw = sout.strip()
        self.LOG.info("Default GW: {0}".format(str(default_gw)))

        self.LOG.info("Verify if sonata_file exists on /etc")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("[ -f /etc/sonata_file ] && echo OK")
        sout = ssh_stdout.read().decode('utf-8').strip()
        serr = ssh_stderr.read().decode('utf-8').strip()

        if sout != "OK":
            self.LOG.info("Configure route for FSM IP")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                "sudo /usr/sbin/route add -net {0} netmask 255.255.255.255 gw {1}"
                .format(fsm_ip, default_gw))
            sout = ssh_stdout.read().decode('utf-8').strip()
            serr = ssh_stderr.read().decode('utf-8').strip()
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo su -c '>> /etc/sonata_file'")
            sout = ssh_stdout.read().decode('utf-8').strip()
            serr = ssh_stderr.read().decode('utf-8').strip()
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("stdout: {0}\nstderr:  {1}"
            .format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))

        # remove default GW
        self.LOG.info("Delete default GW")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /usr/sbin/route del default gw {0}".format(default_gw))
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))

        # next VNF exists
        if next_ip is not None:
            # find virtual link of vpn output
            self.LOG.info("cpmgmt IP address:'{0}'; cpinput IP address:'{1}'; forward_cpinput_ip:'{2}'"
                .format(host_ip, data_ip, next_ip))

            self.LOG.info("Set the path to the next hop by eth1 (output)")
            #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /usr/sbin/ip route add {0}/32 dev eth2".format(next_ip))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /usr/sbin/ip route add {0}/32 dev eth1".format(next_ip))
            sout = ssh_stdout.read().decode('utf-8')
            serr = ssh_stderr.read().decode('utf-8')
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

            self.LOG.info("Configure default GW for next VNF VM in chain using the eth2 (output) interface")
            #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /usr/sbin/route add default gw {0} dev eth2".format(next_ip))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /usr/sbin/route add default gw {0} dev eth1".format(next_ip))
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))
        else:
            self.LOG.info("Modify DHCP configuration of interfaces")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo sed -i \"/DEFROUTE/cDEFROUTE=\"no\"\" /etc/sysconfig/network-scripts/ifcfg-eth0")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo sed -i \"/DEFROUTE/cDEFROUTE=\"yes\"\" /etc/sysconfig/network-scripts/ifcfg-eth1")
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/ifconfig eth1 | grep \"inet\" | awk '{ if ($1 == \"inet\") {print $2} }'")
            last_if = ssh_stdout.read().decode('utf-8').strip().split(".")
            self.LOG.info("Last interface = {0}".format(last_if))
            last_if[3] = str((int(last_if[3]) & 224) + 1)

            self.LOG.info("Add default route for input/output interface (eth1)")
            #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo dhclient -r eth2 && dhclient eth2")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo dhclient -r eth1 && dhclient eth1")
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /usr/sbin/route add default gw {0}".format('.'.join(last_if)))
            self.LOG.info("stdout: {0}\nstderr:  {1}" .format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))


        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo sed -i \'s/#net.ipv4.ip_forward/net.ipv4.ip_forward/g\' /etc/sysctl.conf")
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))
        
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo systemctl restart network.service")
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))

  
class Ubuntu_implementation(OS_implementation):
    
    def __init__(self, logger):
        self.LOG = logger
  
    def configure_interfaces(self, ssh):
        self.LOG.info("configure_interfaces Ubuntu")
        
        if ssh == None:
            return;
        
        self.LOG.info("Disable UFW service")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo systemctl stop ufw && sudo systemctl disable ufw")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')

        self.LOG.info("Copy net interfaces cfg files")
        ftp = ssh.open_sftp()
        self.LOG.info("SFTP connection established")

        localpath = self.config_dir + '/50-cloud-init.cfg'
        self.LOG.info("SFTP connection entering on %s", localpath)
        remotepath = '/tmp/50-cloud-init.cfg'
        sftpa = ftp.put(localpath, remotepath)
        ftp.close()

        self.LOG.info("Making sure .ssh directory exists")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("[ -d .ssh ] && echo OK")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
        if sout != "OK":
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("mkdir .ssh")
            sout = ssh_stdout.read().decode('utf-8')
            serr = ssh_stderr.read().decode('utf-8')
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("chmod 700 .ssh")
            sout = ssh_stdout.read().decode('utf-8')
            serr = ssh_stderr.read().decode('utf-8')
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Making sure the hostname is resolvable")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('echo "127.0.0.1 $(hostname)" | sudo tee -a /etc/hosts')
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Copying scripts")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo cp /tmp/50-cloud-init.cfg /etc/network/interfaces.d")
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Displaying eth1 data")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/sbin/ifconfig eth1")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Displaying eth2 data")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/sbin/ifconfig eth2")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Displaying eth3 data")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/sbin/ifconfig eth3")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Force ip forwarding")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("echo '1' | sudo tee /proc/sys/net/ipv4/ip_forward")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Get eth1 (input) subnetwork")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/sbin/ip route list | grep -m 1 '/27 dev eth1' | awk '{printf \"%s\",$1}'")
        input_subnetwork = ssh_stdout.read().decode('utf-8').strip()
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(input_subnetwork, serr))

        self.LOG.info("Delete extraneous rule on eth2 (output)")
        #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/ip route del {0} dev eth2".format(input_subnetwork))
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/ip route del {0} dev eth1".format(input_subnetwork))
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        self.LOG.info("Get current default GW")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/sbin/ip route | awk '/default/ { print $3 }'")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
        return sout.strip()

    def configure_quagga_forwarding_rules(self, ssh, gw):

        self.LOG.info("Always use eth0 (mgmt) for connection to 10.230.x.x for protecting admin ssh connections")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "sudo /sbin/ip route add 10.230.0.0/16 dev eth0 via {0}".format(gw))
        # FIX: how to known that eth0 is always mgmt ?
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))

        self.LOG.info('get own ip')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/sbin/ifconfig eth0 | grep \"inet\" | awk '{ if ($1 == \"inet\") {print $2} }' | cut -b 6-")
        my_ip = ssh_stdout.read().decode('utf-8').strip()
        self.LOG.info('stdout from remote: ' + my_ip)
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info('Port 80 to 3128 for {0}'.format(my_ip))
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/iptables -t nat -A PREROUTING -i eth1 -p tcp -m tcp --dport 80 -j DNAT --to-destination '{0}:3128'".format(my_ip))
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Redirecting port")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo /sbin/iptables -t nat -A PREROUTING -i eth1 -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 3128')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Setting masquerade")
        #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo /sbin/iptables -t nat -A POSTROUTING -o eth2 -j MASQUERADE')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo /sbin/iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

        self.LOG.info("Accept in the filter table")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo /sbin/iptables -t filter -A INPUT -p tcp --dport 3128 -j ACCEPT')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))
        
        self.LOG.info("Configuration of quagga service")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl start quagga')
        self.LOG.info('stdout from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('stderr from remote: ' + ssh_stderr.read().decode('utf-8'))

    def reconfigure_service(self, ssh, cfg):
        self.LOG.info("SSH connection established")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl stop quagga')
        self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('output from remote: ' + ssh_stderr.read().decode('utf-8'))
        
        ftp = ssh.open_sftp()
        self.LOG.info("SFTP connection established")

        if cfg == "transparent":
            localpath = self.config_options[cfg]
            self.LOG.info("SFTP connection entering on %s", localpath)
            remotepath = '/tmp/quagga.conf'
            sftpa = ftp.put(localpath, remotepath)
        elif cfg == "squidguard":
            cfg = "squidufdb_xenial"
            localpath = self.config_options[cfg]
            self.LOG.info("SFTP connection entering on %s", localpath)
            remotepath = '/tmp/quagga.conf'
            sftpa = ftp.put(localpath, remotepath)
            localpath = self.config_options["ufdbguardconf"]
            self.LOG.info("SFTP connection entering on %s", localpath)
            remotepath = '/tmp/ufdbguard.conf'
            sftpa = ftp.put(localpath, remotepath)
        ftp.close()

        self.LOG.info("Moving the Squid configuration file")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo mv /etc/quagga/quagga.conf /etc/quagga/quagga.conf.old')
        self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('output from remote: ' + ssh_stderr.read().decode('utf-8'))
        self.LOG.info("Copying the Squid configuration file")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo cp /tmp/quagga.conf /etc/quagga')
        self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('output from remote: ' + ssh_stderr.read().decode('utf-8'))

        if cfg == "squidufdb_xenial":
            self.LOG.info("Copying the Squid Guard configuration file")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("[ -f /usr/local/ufdbguard/etc/ufdbGuard.conf ] && echo OK")
            sout = ssh_stdout.read().decode('utf-8')
            self.LOG.info('output from remote: ' + sout)
            self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))

            if sout == "OK":
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo su -c 'mv /usr/local/ufdbguard/etc/ufdbGuard.conf /usr/local/ufdbguard/etc/ufdbGuard.conf.old'") 
                self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
                self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))
            
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo su -c 'mv /tmp/ufdbguard.conf /usr/local/ufdbguard/etc/ufdbGuard.conf'")
            self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
            self.LOG.info('error from remote: ' + ssh_stderr.read().decode('utf-8'))

            self.LOG.info("Restarting ufdb")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl start ufdb.service')
            self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
            self.LOG.info('output from remote: ' + ssh_stderr.read().decode('utf-8'))


        self.LOG.info("Restarting Squid")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo systemctl restart quagga')
        self.LOG.info('output from remote: ' + ssh_stdout.read().decode('utf-8'))
        self.LOG.info('output from remote: ' + ssh_stderr.read().decode('utf-8'))

    def configure_forward_routing(self, ssh, host_ip, data_ip, next_ip):
        self.LOG.info("Retrieve FSM IP address")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "FSM_IP=$(echo $SSH_CLIENT | awk '{ print $1}') && echo $FSM_IP")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
        fsm_ip = sout.strip()
        self.LOG.info("FSM IP: {0}".format(fsm_ip))

        self.LOG.info("Get current default GW")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "IP=$(/sbin/ip route | awk '/default/ { print $3 }') && echo $IP")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
        default_gw = sout.strip()
        self.LOG.info("Default GW: {0}".format(str(default_gw)))

        self.LOG.info("Verify if sonata_file exists on /etc")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("[ -f /etc/sonata_file ] && echo OK")
        sout = ssh_stdout.read().decode('utf-8').strip()
        serr = ssh_stderr.read().decode('utf-8').strip()

        if sout != "OK":
            self.LOG.info("Configure route for FSM IP")
            
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                "sudo /sbin/route add -net {0} netmask 255.255.255.255 gw {1}"
                .format(fsm_ip, default_gw))
            sout = ssh_stdout.read().decode('utf-8').strip()
            serr = ssh_stderr.read().decode('utf-8').strip()
            
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo su -c '>> /etc/sonata_file'")
            sout = ssh_stdout.read().decode('utf-8').strip()
            serr = ssh_stderr.read().decode('utf-8').strip()
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        # remove default GW
        self.LOG.info("Delete default GW")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "sudo /sbin/route del default gw {0}".format(default_gw))
        sout = ssh_stdout.read().decode('utf-8').strip()
        serr = ssh_stderr.read().decode('utf-8').strip()
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        # next VNF exists
        if next_ip is not None:
            # find virtual link of vpn output
            self.LOG.info("cpmgmt IP address:'{0}'; cpinput IP address:'{1}'; forward_cpinput_ip:'{2}'"
                .format(host_ip, data_ip, next_ip))

            self.LOG.info("Force the path to the next hope to go through eth1 (output)")
            #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/ip route add {0}/32 dev eth2".format(next_ip))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/ip route add {0}/32 dev eth1".format(next_ip))
            sout = ssh_stdout.read().decode('utf-8')
            serr = ssh_stderr.read().decode('utf-8')
            self.LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

            self.LOG.info("Configure default GW for next VNF VM in chain using the eth2 (output) interface")
            #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/route add default gw {0} dev eth2".format(next_ip))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/route add default gw {0} dev eth1".format(next_ip))
            self.LOG.info("stdout: {0}\nstderr:  {1}"
                     .format(ssh_stdout.read().decode('utf-8'),
                             ssh_stderr.read().decode('utf-8')))
        else:
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/ifconfig eth1 | grep \"inet\" | awk '{if($1==\"inet\") { print $2; }}' | cut -b 6-")
            last_if = ssh_stdout.read().decode('utf-8').strip().split(".")
            self.LOG.info("Last interface = {0}".format(last_if))
            last_if[3] = str((int(last_if[3]) & 224) + 1)
            str_out = "supersede routers {0};".format('.'.join(last_if))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo su -c 'echo {0} >>  /etc/dhcp/dhclient.conf'".format(str_out))
            self.LOG.info("stdout: {0}\nstderr:  {1}"
                     .format(ssh_stdout.read().decode('utf-8'),
                             ssh_stderr.read().decode('utf-8')))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /sbin/route add default gw {0}".format('.'.join(last_if)))
            self.LOG.info("stdout: {0}\nstderr:  {1}"
                     .format(ssh_stdout.read().decode('utf-8'),
                             ssh_stderr.read().decode('utf-8')))

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo sed -i \'s/#net.ipv4.ip_forward/net.ipv4.ip_forward/g\' /etc/sysctl.conf")
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))
        
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo /etc/init.d/procps restart")
        self.LOG.info("stdout: {0}\nstderr:  {1}".format(ssh_stdout.read().decode('utf-8'), ssh_stderr.read().decode('utf-8')))
