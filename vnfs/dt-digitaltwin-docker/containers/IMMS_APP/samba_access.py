#!/bin/bash
#  Copyright (c) 2018 5GTANGO, Weidmüller, Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, 5GTANGO, Weidmüller, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).

# code from https://pysmb.readthedocs.io/en/latest/api/smb_SMBConnection.html
import os
import time
import datetime
import tempfile
from pathlib import Path
from smb.SMBConnection import SMBConnection


class SambaAccess:
    def __init__(self, smb_host, smb_share="guest", local_dir=Path("../em63_share")):
        self.smb_host = smb_host
        self.smb_share = smb_share
        self.local_dir = local_dir

    def samba_connect(self):
        """Connect to Samba host. Block and retry forever if connection times out"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # username, password, my_name, remote_name seem to not matter when creating the connection; only the host IP
        conn = SMBConnection("guest", "", "", "")
        
        print("\nConnecting to SMB host {} at time {}".format(self.smb_host, timestamp), flush=True)
        try:
            conn.connect(self.smb_host, 139, timeout=10)
        except: 
            print("Connection timed out. Retry in 5s")
            time.sleep(5)
            return self.samba_connect()
 
        return conn 
        
    def list_files(self):
        """Print name of all files and directories in the Samba share"""
        conn = self.samba_connect()
        print("Listing files and dirs in Samba share:", flush=True)
        file_list = conn.listPath(self.smb_share, "")
        for f in file_list:
            print(f.filename, flush=True)
            
    def get_file(self, filename, return_content=False):
        """
        Retrievs and saves specified file from Samba share locally. 
        Returns path to downloaded file (default). Or file contents (if return_content=True).
        """
        conn = self.samba_connect()
        #file_obj = tempfile.NamedTemporaryFile()
        file_path = os.path.join(self.local_dir, filename)
        file_obj = open(file_path, 'wb')
        file_attr, filesize = conn.retrieveFile(self.smb_share, filename, file_obj)        
        file_obj.close()
        
        if return_content:
            with open(file_path, 'r') as f:
                return f.read()
        return file_path
                    
        
if __name__ == "__main__":
    # specify floating IP of NS2 MDC
    smb = SambaAccess("10.200.16.14")
    smb.list_files()
    smb_file = smb.get_file("00010010.JOB", return_content=True)
    print(smb_file)

