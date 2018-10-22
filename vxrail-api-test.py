#!/usr/bin/python

import sys
import requests

# disable warnings from SSL Check
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

import requests

url = "https://172.168.10.150/rest/vxm/v1/system"

response = requests.request("GET", url, verify=False, auth=('administrator@vsphere.local', 'VxR@il1!'))

print(response.text)

# vxrm APIS

# GET https://<VxM IP>/rest/vxm/v1/system
