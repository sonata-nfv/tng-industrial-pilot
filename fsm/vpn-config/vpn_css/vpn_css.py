"""
Copyright (c) 2015 SONATA-NFV
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).
"""

import time
import logging
import yaml
import paramiko
import os
import sys
import tempfile
import configparser
from collections import namedtuple
from sonsmbase.smbase import sonSMbase
from .ssh import Client

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class CssFSM(sonSMbase):

    _listening_topic_root = ('generic', 'fsm')

    @staticmethod
    def get_listening_topic_name():
        return '.'.join(CssFSM._listening_topic_root)

    def __init__(self):

        """
        :param specific_manager_type: specifies the type of specific manager
        that could be either fsm or ssm.
        :param service_name: the name of the service that this specific manager
        belongs to.
        :param function_name: the name of the function that this specific
        manager belongs to, will be null in SSM case
        :param specific_manager_name: the actual name of specific manager
        (e.g., scaling, placement)
        :param id_number: the specific manager id number which is used to
        distinguish between multiple SSM/FSM that are created for the same
        objective (e.g., scaling with algorithm 1 and 2)
        :param version: version
        :param description: description
        """

        LOG.debug('Initialize CssFSM from %s', __file__)
        self.specific_manager_type = 'fsm'
        self.service_name = 'psaservice'
        self.function_name = 'vpn-vnf'
        self.specific_manager_name = 'vpn-config'
        self.id_number = '1'
        self.version = 'v0.1'
        self.topic = ''
        self.description = "An FSM that subscribes to start, stop and configuration topic"
        self.is_running_in_emulator = 'SON_EMULATOR' in os.environ
        LOG.debug('Running in the emulator is %s', self.is_running_in_emulator)
# variable to protect specific route to FSM config

        self.FSMroute = False

        super(self.__class__, self).__init__(specific_manager_type=self.specific_manager_type,
                                             service_name=self.service_name,
                                             function_name=self.function_name,
                                             specific_manager_name=self.specific_manager_name,
                                             id_number=self.id_number,
                                             version=self.version,
                                             description=self.description)

    def on_registration_ok(self):

        # The fsm registration was successful
        LOG.debug("Received registration ok event.")

        # send the status to the SMR
        status = 'Subscribed, waiting for alert message'
        message = {'name': self.specific_manager_id,
                   'status': status}
        self.manoconn.publish(topic='specific.manager.registry.ssm.status',
                              message=yaml.dump(message))

        # Subscribing to the topics that the fsm needs to listen on
#        topic = CssFSM.get_listening_topic_name()
        self.topic = 'generic.fsm.' + self.sfuuid
        self.manoconn.subscribe(self.message_received, self.topic)
        LOG.info("Subscribed to " + self.topic + " topic.")

    def message_received(self, ch, method, props, payload):
        """
        This method handles received messages
        """

        LOG.debug('<-- message_received app_id=%s', props.app_id)
        # Decode the content of the message
        request = yaml.load(payload)

        # Don't trigger on non-request messages
        if "fsm_type" not in request.keys():
            LOG.info("Received a non-request message, ignoring...: request=%s", request)
            return
        LOG.info('Handling message with fsm_type=%s', request["fsm_type"])

        # Create the response
        response = None

        # the 'fsm_type' field in the content indicates for which type of
        # fsm this message is intended. In this case, this FSM functions as
        # start, stop and configure FSM
        if str(request["fsm_type"]) == "start":
            LOG.info("Start event received: " + str(request["content"]))
            response = self.start_event(request["content"])

        if str(request["fsm_type"]) == "stop":
            LOG.info("Stop event received: " + str(request["content"]))
            response = self.stop_event(request["content"])

        if str(request["fsm_type"]) == "configure":
            LOG.info("Config event received: " + str(request["content"]))
            response = self.configure_event(request["content"])

        if str(request["fsm_type"]) == "scale":
            LOG.info("Scale event received: " + str(request["content"]))
            response = self.scale_event(request["content"])

        # If a response message was generated, send it back to the FLM
        if response is not None:
            # Generated response for the FLM
            LOG.info("Response to request generated:" + str(response))
            # topic = CssFSM.get_listening_topic_name()
            corr_id = props.correlation_id
            self.manoconn.notify(self.topic,
                                 yaml.dump(response),
                                 correlation_id=corr_id)
            return

        # If response is None:
        LOG.info("Request received for other type of FSM, ignoring...")

    def start_event(self, content):
        """
        This method handles a start event.
        """
        LOG.info("Performing life cycle start event")
        LOG.info("content: " + str(content.keys()))
        # TODO: Add the start logic. The content is a dictionary that contains
        # the required data

        vnfr = content["vnfr"]
        vnfd = content["vnfd"]
        LOG.info("VNFR: " + yaml.dump(vnfr))

        vdu = vnfr['virtual_deployment_units'][0]
        cps = vdu['vnfc_instance'][0]['connection_points']

        mgmt_ip = None
        for cp in cps:
            if cp['type'] == 'management':
                mgmt_ip = cp['interface']['address']
                LOG.info("management ip: " + str(mgmt_ip))

        if not mgmt_ip:
            LOG.info("No management connection point in vnfr")
            return

        username = "root"
        password = "sonata"
        sp_ip = '10.30.0.112'

        # Configuring the monitoring probe
        ssh_client = Client(mgmt_ip, 'sonata', 'sonata', LOG)
        LOG.info('Mon Config: Create new conf file')
        self.createConf(sp_ip, 4, 'vpn-vnf')
        ssh_client.sendFile('node.conf')
        ssh_client.sendCommand('ls /tmp/')
        ssh_client.sendCommand('sudo mv /tmp/node.conf /opt/Monitoring/node.conf')
        ssh_client.sendCommand('sudo systemctl restart mon-probe.service')
        ssh_client.close()
        LOG.info('Mon Config: Completed')

        ssh = paramiko.SSHClient()
        LOG.info("SSH client started")

        # allows automatic adding of unknown hosts to 'known_hosts'
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(mgmt_ip, username=username, password=password)
        LOG.info("SSH connection established")

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls')
        LOG.info('output from remote: ' + str(ssh_stdout))
        LOG.info('output from remote: ' + str(ssh_stdin))
        LOG.info('output from remote: ' + str(ssh_stderr))

        LOG.info("Get current default GW")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "IP=$(/sbin/ip route | awk '/default/ { print $3 }') && echo $IP")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(sout, serr))
        default_gw = sout.strip()

        LOG.info("Always use ethO (mgmt) for connection from 10.230.x.x for protecting ssh connections")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "/sbin/ip route add 10.230.0.0/16 dev eth0 via {0}".format(default_gw))
        # FIX: how to tell that eth0 is mgmt
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(ssh_stdout.read().decode('utf-8'),
                         ssh_stderr.read().decode('utf-8')))

        LOG.info("Make the vpn server supports multiple client")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "echo 'duplicate-cn' | sudo tee -a /etc/openvpn/server.conf")
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(ssh_stdout.read().decode('utf-8'),
                         ssh_stderr.read().decode('utf-8')))

        LOG.info("Make the vpn use tcp for the tunnel")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "sudo sed -i 's/proto udp/proto tcp/g' /etc/openvpn/server.conf")
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(ssh_stdout.read().decode('utf-8'),
                         ssh_stderr.read().decode('utf-8')))

        LOG.info("Restart the vpn server")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "sudo systemctl restart openvpn@server.service")
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(ssh_stdout.read().decode('utf-8'),
                         ssh_stderr.read().decode('utf-8')))

        # Create a response for the FLM
        response = {}
        response['status'] = 'COMPLETED'

        # TODO: complete the response

        return response

    def stop_event(self, content):
        """
        This method handles a stop event.
        """
        LOG.info("Performing life cycle stop event")
        LOG.info("content: " + str(content.keys()))
        # TODO: Add the stop logic. The content is a dictionary that contains
        # the required data

        vnfr = content['vnfr']

        # Create a response for the FLM
        response = {}
        response['status'] = 'COMPLETED'

        # TODO: complete the response

        return response

    def configure_event(self, content):
        """
        This method handles a configure event.
        """
        LOG.info("Performing life cycle configure event")
        LOG.info("content: " + str(content.keys()))

        if not content['next_ip']:
            result = self.vpn_configure(content['management_ip'],
                                        content['own_ip'])

        else:
            result = self.vpn_configure(content['management_ip'],
                                        content['own_ip'],
                                        next_ip=content['next_ip'])

        # Create a response for the FLM
        response = dict()
        response['status'] = 'COMPLETED' if result else 'ERROR'

        # TODO: complete the response

        return response

    def scale_event(self, content):
        """
        This method handles a scale event.
        """
        LOG.info("Performing life cycle scale event")
        LOG.info("content: " + str(content.keys()))
        # TODO: Add the configure logic. The content is a dictionary that
        # contains the required data

        # Create a response for the FLM
        response = {}
        response['status'] = 'COMPLETED'

        # TODO: complete the response

        return response

    def vpn_configure(self, mgmt_ip, own_ip, next_ip=None):

        LOG.info("management ip: " + str(mgmt_ip))
        LOG.info("in/out ip: " + str(own_ip))

        # connection to vpn vm

        username = "root"
        password = "sonata"

        ssh = paramiko.SSHClient()
        LOG.info("SSH client started")

        # allows automatic adding of unknown hosts to 'known_hosts'
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(mgmt_ip, username=username, password=password)
        LOG.info("SSH connection established")

        LOG.info("run ifconfig:")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "ifconfig")
        sout = ssh_stdout.read().decode('utf-8')
        LOG.info("{}".format(sout))

        LOG.info("Retrieve FSM IP address")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "FSM_IP=$(echo $SSH_CLIENT | awk '{ print $1}') && echo $FSM_IP")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(sout, serr))
        fsm_ip = sout.strip()
        LOG.info("FSM IP: {0}".format(fsm_ip))

        LOG.info("Get current default GW")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "IP=$(/sbin/ip route | awk '/default/ { print $3 }') && echo $IP")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(sout, serr))
        default_gw = sout.strip()
        LOG.info("Default GW: {0}".format(str(default_gw)))

# Change to establish route for FSM config - only done once
        if self.FSMroute == False:
            LOG.info("Configure route for FSM IP")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                "route add -net {0} netmask 255.255.255.255 gw {1}"
                .format(fsm_ip, default_gw))
            LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(ssh_stdout.read().decode('utf-8'),
                         ssh_stderr.read().decode('utf-8')))
            self.FSMroute = True

        # remove default GW
        LOG.info("Delete default GW")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "route del default gw {0}".format(default_gw))
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(ssh_stdout.read().decode('utf-8'),
                         ssh_stderr.read().decode('utf-8')))

        # next VNF exists
        if next_ip:
            LOG.info("Configure default GW for next VNF VM (IP={0})in chain"
                     .format(next_ip))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                "route add default gw {0}".format(next_ip))
            LOG.info("stdout: {0}\nstderr:  {1}"
                     .format(ssh_stdout.read().decode('utf-8'),
                             ssh_stderr.read().decode('utf-8')))

        # next VNF doesn't exist
        else:
            LOG.info("Modify DHCP configuration of interfaces")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                "sed -i \"/DEFROUTE/cDEFROUTE=\"no\"\" /etc/sysconfig/network-scripts/ifcfg-eth0"
            )
            LOG.info("stdout: {0}\nstderr:  {1}"
                     .format(ssh_stdout.read().decode('utf-8'),
                             ssh_stderr.read().decode('utf-8')))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                "sed -i \"/DEFROUTE/cDEFROUTE=\"yes\"\" /etc/sysconfig/network-scripts/ifcfg-eth1"
            )
            LOG.info("stdout: {0}\nstderr:  {1}"
                     .format(ssh_stdout.read().decode('utf-8'),
                             ssh_stderr.read().decode('utf-8')))

            LOG.info("Add default route for input/output interface (eth1)")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                "dhclient")
            LOG.info("stdout: {0}\nstderr:  {1}"
                     .format(ssh_stdout.read().decode('utf-8'),
                             ssh_stderr.read().decode('utf-8')))

        LOG.info("Run iptables config")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "/root/iptables.sh")
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(ssh_stdout.read().decode('utf-8'),
                         ssh_stderr.read().decode('utf-8')))

        # Configure DNS correctly
        LOG.info("Configure appropriate DNS'")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            "printf \"NETWORKING=yes\\nNOZEROCONF=yes\\nDNS1=8.8.8.8\\nDNS2=8.8.4.4\" > /etc/sysconfig/network"
        )
        LOG.info("stdout: {0}\nstderr:  {1}"
                 .format(ssh_stdout.read().decode('utf-8'),
                         ssh_stderr.read().decode('utf-8')))

        # Create a response for the FLM
        response = {}
        response['status'] = 'COMPLETED'
        return response

    def createConf(self, pw_ip, interval, name):

        config = configparser.RawConfigParser()
        config.add_section('vm_node')
        config.add_section('Prometheus')
        config.set('vm_node', 'node_name', name)
        config.set('vm_node', 'post_freq', interval)
        config.set('Prometheus', 'server_url', 'http://'+pw_ip+':9091/metrics')
    
    
        with open('node.conf', 'w') as configfile:    # save
            config.write(configfile)
    
        f = open('node.conf', 'r')
        LOG.debug('Mon Config-> '+"\n"+f.read())
        f.close()
        

        # configure vm using ansible playbook
        # loader = DataLoader()
        # with tempfile.NamedTemporaryFile() as fp:
        #     fp.write(b'[vpnserver]\n')
        #     if self.is_running_in_emulator:
        #         fp.write(b'mn.vnf_vpn')
        #     else:
        #         fp.write(mgmt_ip.encode('utf-8'))
        #     fp.flush()
        #     inventory = InventoryManager(loader=loader, sources=[fp.name])
        # variable_manager = VariableManager(loader=loader, inventory=inventory)
        #
        # playbook_path = os.path.abspath('./ansible/site.yml')
        # LOG.debug('Targeting the ansible playbook: %s', playbook_path)
        # if not os.path.exists(playbook_path):
        #     LOG.error('The playbook does not exist')
        #     return False
        #
        # Options = namedtuple('Options',
        #                      ['listtags', 'listtasks', 'listhosts',
        #                       'syntax', 'connection', 'module_path',
        #                       'forks', 'remote_user', 'private_key_file',
        #                       'ssh_common_args', 'ssh_extra_args',
        #                       'sftp_extra_args', 'scp_extra_args',
        #                       'become', 'become_method', 'become_user',
        #                       'verbosity', 'check', 'diff'])
        # options = Options(listtags=False, listtasks=False, listhosts=False,
        #                   syntax=False, connection='ssh', module_path=None,
        #                   forks=100, remote_user='slotlocker',
        #                   private_key_file=None, ssh_common_args=None,
        #                   ssh_extra_args=None, sftp_extra_args=None,
        #                   scp_extra_args=None, become=True,
        #                   become_method=None, become_user='root',
        #                   verbosity=None, check=False, diff=True)
        # if self.is_running_in_emulator:
        #     options = options._replace(connection='docker', become=False)
        #
        # variable_manager.extra_vars = {'LOCAL_IP_ADDRESS': cpinput_ip,
        #                                'SON_EMULATOR': self.is_running_in_emulator }
        #
        # passwords = {}
        #
        # pbex = PlaybookExecutor(playbooks=[playbook_path],
        #                         inventory=inventory,
        #                         variable_manager=variable_manager,
        #                         loader=loader, options=options,
        #                         passwords=passwords)
        #
        # results = pbex.run()
        # LOG.debug('Results from ansible = %s, %s', results, type(results))
        # return results == 0


def main(working_dir=None):
    if working_dir:
        os.chdir(working_dir)
    LOG.info('Welcome to the main in %s', __name__)
    CssFSM()
    while True:
        time.sleep(10)


if __name__ == '__main__':
    main()
