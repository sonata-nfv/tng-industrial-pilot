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

import os
import time
import logging
import tempfile
import yaml
import paramiko
from IPy import IP
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from sonsmbase.smbase import sonSMbase
from .OS_Factory import Factory, OS_implementation

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

class faceFSM(sonSMbase):

    config_options = { 'direct': './ansible/roles/squid/files/squid_direct.conf', 
        'transparent': './ansible/roles/squid/files/squid.conf', 
        'squidguard': './ansible/roles/squid/files/squid_guard.conf' }
    config_dir = './ansible/roles/squid/files'
    username = 'sonata'
    password = 'sonata'
    with_monitoring = True
    monitoring_ip = '10.30.0.112'
    option = 1

    def __init__(self):
        LOG.debug('Initialization of faceFSM in %s', __file__)
        
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
    
        self.specific_manager_type = 'fsm'
        #self.service_name = 'psa'
        #self.function_name = 'proxy'
        self.specific_manager_name = 'prx-config'
        self.service_name = 'psaservice'
        self.function_name = 'prx-vnf'
        self.id_number = '1'
        self.version = 'v0.1'
        self.description = 'FSM that implements the subscription of the start, stop, configuration topics'
        self.topic = ''
        self.os_factory = Factory()

                
        super(self.__class__, self).__init__(specific_manager_type = self.specific_manager_type,
                                             service_name = self.service_name,
                                             function_name = self.function_name,
                                             specific_manager_name = self.specific_manager_name,
                                             id_number = self.id_number,
                                             version = self.version,
                                             description = self.description)

    def on_registration_ok(self):
        LOG.debug("Received registration ok event for %s", __file__)
        
        state = "Subscription successful, I'm waiting for messages"
        message = {'name': self.specific_manager_id,
                   'status': state}
        self.manoconn.publish(topic = 'specific.manager.registry.ssm.status',
                              message = yaml.dump(message))
        self.topic = "generic.fsm." + str(self.sfuuid)
        self.manoconn.subscribe(self.message_received, self.topic)
        LOG.info("Subscribed to " + self.topic + " topic.")
        
    def message_received(self, ch, method, props, payload):
        LOG.debug("Received message in %s", __file__)
        """
        handling of the different possible messages
        """
        
        request = yaml.load(payload)
        if "fsm_type" not in request.keys():
            LOG.info("Received a non-request message, ignoring...")
            return
        
        response = None
        
        if str(request["fsm_type"]) == "start":
            LOG.info("Start event received: " + str(request["content"]))
            response = self.start_ev(request["content"])
        elif str(request["fsm_type"]) == "stop":
            LOG.info("Stop event received: " + str(request["content"]))
            response = self.stop_ev(request["content"])
        elif str(request["fsm_type"]) == "configure":
            LOG.info("Config event received: " + str(request["content"]))
            response = self.configure_ev(request["content"])
        elif str(request["fsm_type"]) == "scale":
            LOG.info("Scale event received: " + str(request["content"]))
            response = self.scale_ev(request["content"])
            
        if response is not None:
            # Generated response for the FLM
            LOG.info("Response to request generated:" + str(response))
            #topic = "generic.fsm." + str(self.sfuuid)
            corr_id = props.correlation_id
            self.manoconn.notify(self.topic,
                                 yaml.dump(response),
                                 correlation_id = corr_id)
            return
        
        LOG.info("Request received for other type of FSM, ignoring...")
    
    def start_ev(self, content):
        LOG.info("Performing life cycle start event with content = %s", str(content.keys()))
        
        vnfr = content["vnfr"]
        LOG.info("VNFR: " + yaml.dump(vnfr))
        vdu = vnfr['virtual_deployment_units'][0]
        cpts = vdu['vnfc_instance'][0]['connection_points']


        squid_ip = None
        for cp in cpts:
            if cp['type'] == 'management':
                squid_ip = cp['interface']['address']
                LOG.info("management ip: " + str(squid_ip))
                
        if squid_ip is not None:
            plbk = '../ansible/site.yml'
            if self.option == 0:
                self.playbook_execution(plbk, squid_ip)
            else:
                opt = 0
                self.ssh_execution(opt, squid_ip)

        else:
            LOG.info("No management connection point in vnfr")
            
        response = {}
        response['status'] = 'COMPLETED'
        response['IP'] = squid_ip
        
        return response
    
    def stop_ev(self, content):
        LOG.info("Performing life cycle stop event with content = %s", str(content.keys()))
        
        vnfr = content["vnfr"]
        LOG.info("VNFR: " + yaml.dump(vnfr))

        vdu = vnfr['virtual_deployment_units'][0]
        cpts = vdu['vnfc_instance'][0]['connection_points']
        
        squid_ip = None
        for cp in cpts:
            if cp['type'] == 'management':
                squid_ip = cp['interface']['address']
                LOG.info("management ip: " + str(squid_ip))
                
                
        if squid_ip is not None:
            plbk = ''
            if self.option == 0:
                self.playbook_execution(plbk, squid_ip)
            else:
                opt = 1
                self.ssh_execution(opt, squid_ip)
        else:
            LOG.info("No management connection point in vnfr")
            
        response = {}
        response['status'] = 'COMPLETED'
        
        return response
    
    def configure_ev(self, content):
        LOG.info("Configuration event with content = %s", str(content.keys()))
        config_opt = 'transparent'
        
        config_opt = content['configuration_opt']
        squid_ip = content['management_ip']
        next_hop_ip = content['next_ip']
        prx_in_out_ip = content['own_ip']

#        vnfrs = content["vnfrs"]
#        nsr = content['nsr']

#        LOG.info("VNFRS: " + yaml.dump(vnfrs))
        
#        result = None
#        if len(vnfrs) == 1:
        try:
            IP(squid_ip)
            IP(prx_in_out_ip)
        except ValueError:
            LOG.info("Invalid value of management IP or own_IP")
            response = {}
            response['status'] = 'ERROR'
            return

        if next_hop_ip is None:
            self.squid_configure(squid_ip, prx_in_out_ip)
        else:
            self.squid_configure(squid_ip, prx_in_out_ip, next_hop_ip)

        plbk = ''
        if self.option == 0:
            self.playbook_execution(plbk, squid_ip)
        else:
            opt = 2
            LOG.info("config_opt = " + config_opt)
            self.ssh_execution(opt, squid_ip, config_opt)
            
        response = {}
        response['status'] = 'COMPLETED'
        response['IP'] = squid_ip
        
        return response
    
    def scale_ev(self, content):
        LOG.info("Scale event with content = %s", str(content.keys()))
        
        vnfr = content["vnfr"]
        LOG.info("VNFR: " + yaml.dump(vnfr))

        vdu = vnfr['virtual_deployment_units'][0]
        cpts = vdu['vnfc_instance'][0]['connection_points']
        
        squid_ip = None
        for cp in cpts:
            if cp['type'] == 'management':
                squid_ip = cp['interface']['address']
                LOG.info("management ip: " + str(squid_ip))
                
        if squid_ip is not None:
            plbk = ''
            if self.option == 0:
                self.playbook_execution(plbk, squid_ip)
            else:
                opt = 3
                self.ssh_execution(opt, squid_ip)

        else:
            LOG.info("No management connection point in vnfr")
        
        response = {}
        response['status'] = 'COMPLETED'
        response['IP'] = squid_ip

        return response
        
    def playbook_execution(self, playbook, host_ip):
        LOG.info("Executing playbook: %s", playbook)
        
        loader = DataLoader()

        inventory = None
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(host_ip.encode('utf-8'))
            fp.flush()
            inventory = InventoryManager(loader=loader, sources=[fp.name])

        variable_manager = VariableManager(loader = loadder, inventory = inventory)

        if not os.path.exists(playbook):
            LOG.error('The playbook %s does not exist', playbook)
            return

        Options = namedtuple('Options',
                             ['listtags', 'listtasks', 'listhosts',
                              'syntax', 'connection', 'module_path',
                              'forks', 'remote_user', 'private_key_file',
                              'ssh_common_args', 'ssh_extra_args',
                              'sftp_extra_args', 'scp_extra_args',
                              'become', 'become_method', 'become_user',
                              'verbosity', 'check'])
        options = Options(listtags = False, listtasks = False, listhosts = False,
                          syntax = False, connection = 'ssh', module_path = None,
                          forks = 100, remote_user = 'slotlocker',
                          private_key_file = None, ssh_common_args = None,
                          ssh_extra_args = None, sftp_extra_args = None,
                          scp_extra_args = None, become = True,
                          become_method = None, become_user = 'root',
                          verbosity = None, check = False)

        variable_manager.extra_vars = {'hosts': host_ip}

        passwords = {}

        pbex = PlaybookExecutor(playbooks = [playbook],
                                inventory = inventory,
                                variable_manager = variable_manager,
                                loader = loader,
                                options = options,
                                passwords = passwords)
        results = pbex.run()
        return
    
    def ssh_execution(self, function, host_ip, config = 'transparent'):
        LOG.info("Executing ssh connection with function: %s", function)

        num_retries = 20
        
        ssh = paramiko.SSHClient()
        LOG.info("SSH client start for user %s", self.username)

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        retry = 0
        while retry < num_retries:
            try:
                ssh.connect(host_ip, username = self.username, password  = self.password)
                break

            except paramiko.BadHostKeyException:
                LOG.info("%s has an entry in ~/.ssh/known_hosts and it doesn't match" % self.server.hostname)
                retry += 1
            except EOFError:
                LOG.info('Unexpected Error from SSH Connection, retry in 5 seconds')
                time.sleep(10)
                retry += 1
            except:
                LOG.info('SSH Connection refused from %s, will retry in 5 seconds', host_ip)
                time.sleep(10)
                retry += 1

        if retry == num_retries:
            LOG.info('Could not establish SSH connection within max retries')
            return;

        LOG.info("SSH connection established")
            
        LOG.info("Get OS system version")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cat /etc/os-release | awk '/^ID=/ { print }' | cut -b 4-")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        os_impl = self.os_factory.get_os_implementation(sout.strip(), LOG)

        if function == 0:
            gw = os_impl.configure_interfaces(ssh)
            os_impl.configure_squid_forwarding_rules(ssh, gw)

            if self.with_monitoring == True:
                os_impl.configure_monitoring(ssh, self.monitoring_ip)

            ssh.close();

        elif function == 1:
            LOG.info("SSH client stop")
            os_impl.stop_service(ssh)
            ssh.close()

        elif function == 2:
            LOG.info("SSH client configure with config " + config)
            os_impl.reconfigure_service(ssh, config)
            ssh.close()

        elif function == 3:
            LOG.info("SSH client scale")
            os_impl.scale_service(ssh)
            ssh.close()
        else:
            LOG.info("Invalid operation on FSM %s", function)
        
        return

    def squid_configure(self, host_ip, data_ip, next_ip = None):
 
        ssh = paramiko.SSHClient()
        LOG.info("SSH client started")

        # allows automatic adding of unknown hosts to 'known_hosts'
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        num_retries = 20

        retry = 0
        while retry < num_retries:
            try:
                ssh.connect(host_ip, username = self.username, password  = self.password)
                break

            except paramiko.BadHostKeyException:
                LOG.info("%s has an entry in ~/.ssh/known_hosts and it doesn't match" % self.server.hostname)
                retry += 1
            except EOFError:
                LOG.info('Unexpected Error from SSH Connection, retry in 5 seconds')
                time.sleep(10)
                retry += 1
            except:
                LOG.info('SSH Connection refused from %s, will retry in 5 seconds', host_ip)
                time.sleep(10)
                retry += 1

        if retry == num_retries:
            LOG.info('Could not establish SSH connection within max retries')
            return;
        
        LOG.info("Get OS system version")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cat /etc/os-release | awk '/^ID=/ { print }' | cut -b 4-")
        sout = ssh_stdout.read().decode('utf-8')
        serr = ssh_stderr.read().decode('utf-8')
        LOG.info("stdout: {0}\nstderr:  {1}".format(sout, serr))

        os_impl = self.os_factory.get_os_implementation(sout.strip(), LOG)

        LOG.info("SSH connection established")
        os_impl.configure_forward_routing(ssh, host_ip, data_ip, next_ip)
        ssh.close()
        # Create a response for the FLM
        response = {}
        response['status'] = 'COMPLETED'
        return response


def main():
    faceFSM()
    while True:
        time.sleep(10)

if __name__ == '__main__':
    main()
