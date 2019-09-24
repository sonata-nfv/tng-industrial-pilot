'''
Copyright (c) 2015 SONATA-NFV, 2017 5GTANGO
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

Neither the name of the SONATA-NFV, 5GTANGO
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).

This work has been performed in the framework of the 5GTANGO project,
funded by the European Commission under Grant number 761493 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the 5GTANGO
partner consortium (www.5gtango.eu).
'''

import paramiko,socket
import time


class Client(object):
    client = None
    LOG = None
    connected = False

    def __init__(self, address, username, logger, password=None, key_filename=None, retries=1):
        print("Connecting to server.")
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.LOG = logger

        for i in range(retries):
            self.LOG.info("Setting up SSH connection, attempt " + str(i + 1))
            try:
                self.client.connect(address, username=username, password=password, key_filename=key_filename, timeout=5)
                self.connected = True
            except (paramiko.BadHostKeyException) as  exception:
                self.LOG.info("Mon Config:SSH: "+str(exception))
            except (paramiko.AuthenticationException)  as  exception:
                self.LOG.info("Mon Config:SSH: "+str(exception))
            except (paramiko.SSHException)  as  exception:
                self.LOG.info("Mon Config:SSH: "+str(exception))
            except (socket.error)  as  exception:
                self.LOG.info("Mon Config:SHH: "+str(exception))

            if self.connected:
                self.LOG.info("SSH connection established")
                break
            else:
                self.LOG.info("SSH connection failed")
                time.sleep(5)

    def sendFile(self,file):
        if(self.client and self.connected):
            self.LOG.info("Mon Config:SHH:Send file...")
            sftp = self.client.open_sftp()
            sftp.put(file, '/tmp/'+file)
            sftp.close()
        else:
            self.LOG.info("Mon Config:SHH:File sending aborted")

    def sendCommand(self, command):
        if(self.client and self.connected):
            stdin, stdout, stderr = self.client.exec_command('echo " " && '+command)
            while not stdout.channel.recv_exit_status():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata
                    alldata=alldata.decode("utf-8")[2:]
                    self.LOG.info("Mon Config:SHH:{cmd:"+command+",output:"+str(alldata).rstrip()+"}")
                    return str(alldata).rstrip()
        else:
            self.LOG.info("Mon Config:SHH:"+command+" aborted.")

    def close(self):
        self.LOG.info('Mon Config:SHH:Close session')
        self.client.close()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)