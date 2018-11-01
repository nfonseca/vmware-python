#!/usr/bin/python

import sys
from pyVmomi import vim, vmodl
from pyVim import connect
import requests
import jsbeautifier
import json

# disable warnings from SSL Check
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")



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

def endpoint_url(ip, api):
    endpoint = 'https://{0}/rest/vxm/v1/{1}'.format(str(ip), str(api))
    print('xxx', endpoint)

    return endpoint


# Function that takes an argument and calls a set of API based on a list
#

api_list = ['system-health', 'system']


def call_api(url, method):
    creds = ('administrator@vsphere.local', 'VxR@il1!')
    payload = {'types': 'vxm'}
    zzz = {"dryrun": "false"}

    headers = {'Content-type': 'application/json'}

    try:

        #        response = requests.request(method, url, verify=False,
        #                                    auth=creds,json=payload)

        response = requests.post(url, verify=False, headers=headers, params=payload, auth=creds, json=zzz)
        # pprint = jsbeautifier.beautify(response.text)
        # result = print(pprint)
        result = response.status_code
        return print(result)

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

def api_list(ip):

    global method
    x = None

    try:
        ans = True
        while ans:
            print("""
            0. Exit/Quit
            1. System Health
            2. System Info
            3. Support Logs
            4. Cluster Shutdown Dry Run

            """)

            ans = input('What API would you like to call? ')
            if ans == '1':
                api = 'system-health'
                x = endpoint_url(ip, api)
                method = 'GET'
                print('endpoint inside api_list', x)
                break
            elif ans == '2':
                api = 'system'
                x = endpoint_url(ip, api)
                method = 'GET'
                break
            elif ans == '3':  # POST Implementation
                api = 'support/logs'
                x = endpoint_url(ip, api)
                method = 'POST'
                break
            elif ans == '4':  # POST Implementation
                api = 'cluster/shutdown'
                x = endpoint_url(ip, api)
                method = 'POST'
                break

            elif ans == '0':
                print('\n Goodbye')
                ans = None
            else:
                print('\n Not Valid Choice Try again')

    except:
        print('Error on api_list()')

    return x


def main():

    vx = findvxrm()

    # loop over all the VXRM IPs found on the DC by findvxrm() function
    for i in vx:
        print('Checking VxRail Manager: ', i)
        api = api_list(i)
        call_api(api, method)



main()

# Things to improve/implement
# 1- Provide a Selection Menu for the APIs that we are going to run
# 2 - List the VXRMs we want to run 1 by 1 or ALL
# 3 - Add display of whats going on
# 4 - How to deal with GET and POST. So far we only do gets.....
