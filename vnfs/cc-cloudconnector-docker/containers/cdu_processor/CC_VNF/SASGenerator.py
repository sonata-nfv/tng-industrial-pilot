# Original source:
# https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-security
# Modification of original source code

from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib import parse
from hmac import HMAC


class SASGenerator:
    # This script generates an SAS token to comunicate with a device in IoTHub
    # uri := is the device url with following form:
    # {iot_hub_name.azure-devices.net/devices/device_id}
    # key := primary key of device
    # police_name is not needed and can be set to None
    # expiry time is messured in seconds
    def generate_sas_token(uri, key, policy_name, expiry):
        ttl = time() + expiry
        sign_key = "%s\n%d" % ((parse.quote_plus(uri)), int(ttl))
        signature = b64encode(HMAC(b64decode(key),
                                   sign_key.encode('utf-8'), sha256).digest())
        rawtoken = {
            'sr':  uri,
            'sig': signature,
            'se': str(int(ttl))
        }
        if policy_name is not None:
            rawtoken['skn'] = policy_name
        return 'SharedAccessSignature ' + parse.urlencode(rawtoken)
