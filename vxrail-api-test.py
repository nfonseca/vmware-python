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


# Seraches  all Vxrail Manager VMs registered in the DC and returns their IP
# in order to pass as input for the loop to query the APIs.
# should add an exception block when no VXRMs are found
# include a counter for the size of the array of vxrm ip
# if size is zero print no VXRM found

def findvxrm():
    vxrmIPs = []

    try:

        content = si.RetrieveServiceContent()
        containerVM = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

        for vm in containerVM.view:
            if vm.name == 'VxRail Manager':
                vxrmIPs.append(vm.summary.guest.ipAddress)
                lenvxrmIPs = len(vxrmIPs)

        if len(vxrmIPs) == 0:
            print('No VMs VxRail Manager Found in Datacenter: Have they been Renamed ?')

        else:
            print(f'Found: {lenvxrmIPs} VxRail Manager VMs')
    except:

        print('Error Calling Function findvxrm()')

    return vxrmIPs


# Function to modify the URL for the query API.
# Takes the IP and input and returns the modified URL

def modifyurl(ip):
    url = 'https://' + str(ip) + '/rest/vxm/v1/'
    return str(url)


# function that return the endpoint for the API CALL
# Ex:
# https://<VxRail IP address>/rest/vxm/v1/system-health
# https://<VxRail IP address>/rest/vxm/v1/clusters/available-nodes
# https://<VxRail IP address>/rest/vxm/v1/support/logs

def endpoint_url(api):
    endpoint = modifyurl(ip) + str(api)
    return endpoint


# Function that takes an argument and calls a set of API based on a list
#

api_list = ['system-health', 'system']


def call_api(ip, api):
    try:
        api_call = modifyurl(ip) + str(api)
        response = requests.request("GET", api_call, verify=False,
                                    auth=('administrator@vsphere.local', 'VxR@il1!'))

        pprint = jsbeautifier.beautify(response.text)
        result = print(pprint)

        return result

    except:
        print('Error Fetching Information for one VXRM VM:' + str(ip))


#
# function to deal with all the different APIs for VXRM
# needs to deal with POST and GET APIs ....
# this is to replace the need for the user to manually write the api name
# For POST requested we will also have to sort out the details
# we also need to take in account the vxrail manager version as not all APIs are available
# the following function needs to be redesigned. It needs to deal with POST/GET methods and return
# something useful for the call_api() function. So all APIs should be listed here
# shall we use dictionaries ? then we pass the dic values to the call api function ?
# https://medium.com/@anthonypjshaw/python-requests-deep-dive-a0a5c5c1e093

def api_list():
    api = None

    try:
        ans = True
        while ans:
            print("""
            0. Exit/Quit
            1. System Health
            2. System Info
            3. Support Logs

            """)

            ans = input('What API would you like to call? ')
            if ans == '1':
                api = 'system-health'
                break
            elif ans == '2':
                api = 'system'
                break
            elif ans == '3':  # POST Implementation
                api = 'support/logs'
                call = requests.post('https://httpbin.org/post')
                break
            elif ans == '0':
                print('\n Goodbye')
                ans = None
            else:
                print('\n Not Valid Choice Try again')

    except:
        print('error')

    return api


def main():
    #    api = input("Choose API: ")
    api = api_list()
    vx = findvxrm()

    for i in vx:
        print('Checking VxRail Manager: ', i)
        call_api(i, api)


main()

# Things to improve/implement
# 1- Provide a Selection Menu for the APIs that we are going to run
# 2 - List the VXRMs we want to run 1 by 1 or ALL
# 3 - Add display of whats going on
# 4 - How to deal with GET and POST. So far we only do gets.....
