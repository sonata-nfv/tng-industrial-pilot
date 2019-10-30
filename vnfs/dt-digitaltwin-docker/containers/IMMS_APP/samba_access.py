# code from https://pysmb.readthedocs.io/en/latest/api/smb_SMBConnection.html
import time
import datetime
from smb.SMBConnection import SMBConnection


class SambaAccess:
    def __init__(self, smb_host):
        self.smb_host = smb_host

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
        
        
    def list_smb_files(self):
        conn = self.samba_connect()
        print("Listing files and dirs in Samba share:", flush=True)
        file_list = conn.listPath("guest", "")
        for f in file_list:
            print(f.filename, flush=True)
        
        
if __name__ == "__main__":
    smb = SambaAccess("10.200.16.24")
    while True:
        smb.list_smb_files()
        time.sleep(5)
