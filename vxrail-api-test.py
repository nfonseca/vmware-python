#!/usr/bin/python

import sys
from pyVmomi import vim, vmodl
from pyVim import connect
import requests
import jsbeautifier

# disable warnings from SSL Check
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

url = "https://172.168.10.150/rest/vxm/v1/system"

response = requests.request("GET", url, verify=False,
                            auth=('administrator@vsphere.local', 'VxR@il1!'))

pprint = jsbeautifier.beautify(response.text)

print(pprint)

###########################
# Establish VC Connection #
###########################

si = connect.SmartConnectNoSSL(host='172.168.10.149',
                               user='administrator@vsphere.local',
                               pwd='VxR@il1!')

print(si.serverClock)


# function to check if cluster is vxrail or not

def isVxRailCluster():
    return None


# function that searchs for all vxrail managaer Vms registered in DC and returns their IP
# in order to pass as input for the loop to query the APIs.

def findVxRM():
    vxrmIPs = []

    content = si.RetrieveServiceContent()
    containerVM = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

    for vm in containerVM.view:
        if vm.name == 'VxRail Manager':
            vxrmIPs.append(vm.summary.guest.ipAddress)

    #    print(vxrmIPs)

    return vxrmIPs


for i in findVxRM():
    print(i)
# vxrm APIS

# GET https://<VxM IP>/rest/vxm/v1/system
