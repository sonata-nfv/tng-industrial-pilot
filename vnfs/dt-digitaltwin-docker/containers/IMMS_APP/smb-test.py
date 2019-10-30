import urllib
from smb.SMBHandler import SMBHandler
from smb.SMBConnection import SMBConnection


conn = SMBConnection("guest", "", "NB-STSCHN", "MDC")
assert conn.connect("10.200.16.24", 139)

print(conn.listShares())
print(conn.listPath("guest", ""))

print("works")

#opener = urllib.request.build_opener(SMBHandler)

