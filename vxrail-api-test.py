#!/usr/bin/python

import sys
from pyVmomi import vim, vmodl
from pyVim import connect
from datetime import datetime
import ssl
import requests
import jsbeautifier

# disable warnings from SSL Check
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

url = "https://172.168.10.150/rest/vxm/v1/system"

response = requests.request("GET", url, verify=False, auth=('administrator@vsphere.local', 'VxR@il1!'))

pprint = jsbeautifier.beautify(response.text)

print(pprint)

######################
# VC Connection      #
######################

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE
si = connect.SmartConnectNoSSL(host='172.168.10.149', user='administrator@vsphere.local', pwd='VxR@il1!')

print(si.serverClock)


# function to check if cluster is vxrail or not

def isVxRailCluster():
    return None

# need to loop over all registered clusters in the DC
# and run a check
# returns ?
# true if  availableField[41].name='VxRail-VERSION'


# vxrm APIS

# GET https://<VxM IP>/rest/vxm/v1/system
