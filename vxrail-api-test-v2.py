#!/usr/bin/python

import sys

# check the python version needed ro run the script

if sys.version_info.major != 3 or sys.version_info[1] < 6:
    print("This script requires Python version 3.6")
    sys.exit(1)

from pyVmomi import vim, vmodl
from pyVim import connect
import requests
import jsbeautifier

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


# Searches  all Vxrail Manager VMs registered in the DC and returns their IP
# in order to pass as input for the loop to query the APIs.

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
            print(f'Found a Total of: {lenvxrmIPs} VxRail Manager VMs')
    except:

        print('Error Calling Function findvxrm()')

    return vxrmIPs


# Function to modify the URL for the query API.
# Takes the IP and input and returns the modified URL

def modifyurl(ip):
    url = 'https://' + str(ip) + '/rest/vxm/v1/'
    return str(url)


# function that return the endpoint for the API CALL

def endpoint_url(ip, api):
    endpoint = 'https://{0}/rest/vxm/v1/{1}'.format(str(ip), str(api))

    return endpoint

# below function just needs to execute the API call and pass the parameters

def call_api(url, method):
    # common to all requests

    creds = ('administrator@vsphere.local', 'VxR@il1!')
    headers = {'Content-type': 'application/json'}

    try:

        response = requests.request(method, url,
                                    verify=False,
                                    headers=headers,
                                    auth=creds,
                                    json=parameters)

        result = response.status_code
        print(f'API Call {url} Submitted and Return Code is: {response.status_code} \n'
              f'API Response is: {jsbeautifier.beautify(response.text)}')

        # below condition needed to deal with POST requests.
        # we get the request_id and process it in order to track it

        if method == 'POST':

            job_id = response.json()
            # exclude POST requests that fail for x and y reasons like storage full
            if job_id is not None:
                req_id = job_id.get('request_id')

                resp_get_id = requests.request('GET', 'https://' + selection + '/rest/vxm/v1/requests/' + req_id,
                                               verify=False,
                                               auth=creds)

                beauty = jsbeautifier.beautify(resp_get_id.text)

                print('''\t
            ##################################\t
            # The Status of the API CALL is: #\t
            ##################################\t
                ''', beauty)

        return result


    except Exception  as err:
        print('Error: ', err)


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
    global parameters
    call = None

    try:
        ans = True
        while ans:
            print("""
            0. Exit/Quit
            1. System Health
            2. System Info
            3. Support Logs
            4. Cluster Shutdown

            """)

            ans = input('What API would you like to call? ')
            if ans == '1':
                api = 'system-health'
                call = endpoint_url(ip, api)
                method = 'GET'
                parameters = None
                break
            elif ans == '2':
                api = 'system'
                call = endpoint_url(ip, api)
                method = 'GET'
                parameters = None
                break
            elif ans == '3':  # POST Implementation
                api = 'support/logs'
                call = endpoint_url(ip, api)
                method = 'POST'
                parameters = {"types": ["vxm"]}
                break
            elif ans == '4':  # POST Implementation
                api = 'cluster/shutdown'
                call = endpoint_url(ip, api)
                method = 'POST'
                param = input('''Select Operation Type:
                1 - Dry Run Only
                2 - Cluster Shutdown''')
                if param == '1':
                    parameters = {"dryrun": "true"}
                else:
                    parameters = {"dryrun": "false"}
                break
            elif ans == '0':
                print('\nExiting Program ...')
                ans = None
            else:
                print('\n Not Valid Choice Try again')

    except:
        print('Error on api_list()')

    return call


def main():
    global selection
    vx = findvxrm()
    #    selection = input('Select VxRail Manager to use: ')
    #    print(vx)
    for vxrm in vx:
        print(f'VXRM Found with IP: {vxrm}')

    selection = input('Type IP of VxRail Manager to Connect to: ')
    if selection in vx:
        print(vx.index(selection))

        print('Checking VxRail Manager: ', selection)
        api = api_list(selection)
        if api is not None:
            call_api(api, method)


main()

# Things to improve/implement
# 1- Provide a Selection Menu for the APIs that we are going to run. DONE !
# 2 - List the VXRMs we want to run 1 by 1 or ALL
# 3 - Add display of whats going on. DONE !
# 4 - How to deal with GET and POST. DONE !
# 5 - Treat exceptions when VXRM have no IP. Ideally IP should come from vSphere
# 4 - Get VxRail version Info from VC (4.5 vs 4.7) and Cluster Name. Couldn't find that info in the lab
# 5 - Provide options for some arguments used in some APIs ( Cluster Shutdown Dry Run for example) DONE
# 6 - Program should always continue after an execution so we can choose other APIs
# 7 - Selection Menu for the VXRMs we want to query. DONE !
# 8 - Add an option to run the same API on ALL the VXRM.
# 9 - Need to fix the POST request on call_api as we now have multiple vxrail choice. DONE !
# 10 - improve error handling on POTS request like this one. DONE


# What API would you like to call? 3
# API Call https://172.168.10.150/rest/vxm/v1/support/logs Submitted and Return Code is: 500
# API Response is:{
# Traceback (most recent call last):
#     "errorCode": 2,
#     "message": "Insufficient storage capacity."
#   File "C:/Users/Nelson.VXRAIL-JUMP-NEL/PycharmProjects/vmware-python/vxrail-api-calls-v2.py", line 106, in call_api
# }
#     resp_get_id = requests.request('GET', 'https://' + selection + '/rest/vxm/v1/requests/' + req_id,
# TypeError: can only concatenate str (not "NoneType") to str
#
# During handling of the above exception, another exception occurred:
#
# Traceback (most recent call last):
#   File "C:/Users/Nelson.VXRAIL-JUMP-NEL/PycharmProjects/vmware-python/vxrail-api-calls-v2.py", line 213, in <module>
#     main()
#   File "C:/Users/Nelson.VXRAIL-JUMP-NEL/PycharmProjects/vmware-python/vxrail-api-calls-v2.py", line 210, in main
#     call_api(api, method)
#   File "C:/Users/Nelson.VXRAIL-JUMP-NEL/PycharmProjects/vmware-python/vxrail-api-calls-v2.py", line 121, in call_api
#     print('Error Fetching Information for one VXRM VM:' + str(ip))
# NameError: name 'ip' is not defined
#
# Process finished with exit code 1

# 11 - Script should tell required version for python
