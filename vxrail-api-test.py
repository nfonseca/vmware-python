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

# response = requests.request("GET", url, verify=False,
#                            auth=('administrator@vsphere.local', 'VxR@il1!'))

# pprint = jsbeautifier.beautify(response.text)

# print(pprint)

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


# Seraches  all Vxrail Manager VMs registered in the DC and returns their IP
# in order to pass as input for the loop to query the APIs.

def findvxrm():
    vxrmIPs = []

    content = si.RetrieveServiceContent()
    containerVM = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

    for vm in containerVM.view:
        if vm.name == 'VxRail Manager':
            vxrmIPs.append(vm.summary.guest.ipAddress)

    return vxrmIPs


# Function to modify the URL for the query API.
# Takes the IP and input and returns the modified URL

def modifyurl(ip):
    url = 'https://' + str(ip) + '/rest/vxm/v1/'
    return str(url)


# Function that takes an argument and calls a set of API based on a list
#

api_list = ['system-health', 'system']


def call_api(ip, api):
    api_call = modifyurl(i) + api
    response = requests.request("GET", api_call, verify=False,
                                auth=('administrator@vsphere.local', 'VxR@il1!'))
    pprint = jsbeautifier.beautify(response.text)
    print(api_call)
    return pprint


api = input("Choose API: ")

for i in findvxrm():
    print(i)
    print(modifyurl(i))
    print(call_api(i, api))

# vxrm APIS

# GET https://<VxM IP>/rest/vxm/v1/system
