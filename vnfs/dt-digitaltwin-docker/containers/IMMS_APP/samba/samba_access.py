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
import datetime
import socket
import time
from pathlib import Path
from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure


class SambaAccess:
    def __init__(self, smb_host, smb_share="guest", local_dir=Path("../em63_share"), username='Alice', hostname='IMMS'):
        print("Creating SambaAccess with host {}, username {}, hostname {}".format(smb_host, username, hostname))
        self.smb_host = smb_host
        self.smb_share = smb_share
        self.local_dir = local_dir
        self.username = username
        self.hostname = hostname

    def samba_connect(self, conn, max_attempts=10):
        """Connect to Samba host. Block and retry max_attempts if connection times out. Return if successful."""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(max_attempts):
            print("\nConnecting to SMB host {} at time {} (attempt {}/{})".format(self.smb_host, timestamp, i,
                                                                                  max_attempts), flush=True)
            try:
                conn.connect(self.smb_host, 139, timeout=10)
                print("Connection successful.")
                return True
            except (socket.timeout, ConnectionResetError) as ex:
                print("Connection timed out. Retry in 5s. Timeout error: {}".format(str(ex)))
                time.sleep(5)
        print("Connection timed out {} times. Giving up now.".format(max_attempts))
        return False
        
    def print_filenames(self):
        """Print name of all files and directories in the Samba share."""
        # empty password and remote_name
        with SMBConnection(self.username, "", self.hostname, "") as conn:
            if self.samba_connect(conn):
                print("Listing files and dirs in Samba share:", flush=True)
                file_list = conn.listPath(self.smb_share, "")
                for f in file_list:
                    print(f.filename, flush=True)
            
    def get_file_content(self, filename, readlines=False, save_file=False):
        """Retrieve and reads specified file from Samba share, return the contents."""
        with SMBConnection(self.username, "", self.hostname, "") as conn:
            if self.samba_connect(conn):
                file_path = os.path.join(self.local_dir, filename)
                print("Downloading {} from the Samba share to {}".format(filename, file_path), flush=True)
                file_obj = open(file_path, 'wb')
                file_attr, filesize = conn.retrieveFile(self.smb_share, filename, file_obj)
                file_obj.close()

                # read content
                with open(file_path, 'r') as f:
                    if readlines:
                        content = f.readlines()
                    else:
                        content = f.read()
                # clean up: delete file
                if not save_file:
                    os.remove(file_path)
                return content

    def save_file(self, filename, file_path, overwrite=True):
        """Save the local file at file_path to the Samba share with the specified name. Return the bytes written."""
        with SMBConnection(self.username, "", self.hostname, "") as conn:
            if self.samba_connect(conn):
                uploaded_bytes = 0
                print("Saving local file {} to Samba share to {}".format(file_path, filename), flush=True)
                try:
                    with open(file_path, 'rb') as f:
                        uploaded_bytes = conn.storeFile(self.smb_share, filename, f)
                except OperationFailure:
                    if overwrite:
                        print("File exists already, overwriting...", flush=True)
                        self.delete_file(filename)
                        return self.save_file(filename, file_path)
                    else:
                        print("File exists already, NOT overwriting...", flush=True)
                return uploaded_bytes

    def write_file(self, filename, text, save_file=False):
        """Write the specified text to the file."""
        print("Writing to file {}: {}".format(filename, text), flush=True)
        with open(filename, 'w') as f:
            f.write(text)
        self.save_file(filename, filename, overwrite=True)
        if not save_file:
            os.remove(filename)
        
    def delete_file(self, filename):
        """Delete files in the Samba share matching the filename."""
        with SMBConnection(self.username, "", self.hostname, "") as conn:
            if self.samba_connect(conn):
                print("Deleting files matching {} from the Samba share".format(filename), flush=True)
                try:
                    conn.deleteFiles(self.smb_share, filename)
                except OperationFailure as ex:
                    print("Error deleting {}. Does the file exist? Error: {}".format(filename, str(ex)))

    def exists_file(self, filename):
        """Return if the file exists in the Samba share"""
        with SMBConnection(self.username, "", self.hostname, "") as conn:
            if self.samba_connect(conn):
                print("Checking if file {} exists".format(filename))
                exists = False
                try:
                    attr = conn.getAttributes(self.smb_share, filename)
                    exists = attr is not None
                finally:
                    print("{} exists: {}".format(filename, exists))
                    return exists

        
if __name__ == "__main__":
    # some code to test and experiment: specify floating IP of NS2 MDC
    smb = SambaAccess("10.200.16.35")
    smb.print_filenames()
    smb.exists_file('blablala')
    # smb.delete_file('remote_test.txt')
    # print(smb.save_file('remote_test.txt', 'test.txt'))
    # print(smb.save_file('remote_test.txt', 'test.txt'))
    # smb.write_file('remote_test2.txt', 'works really well!')
    # print(smb.get_file("remote_test2.txt", return_content=True))
    # smb.print_filenames()

