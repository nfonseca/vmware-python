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
import subprocess
import platform
import os
import argparse
import getpass

# disable warnings from SSL Check
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")


def findvxrm():
    vxrmIPs = []

    try:

        containerVM = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

        for vm in containerVM.view:
            if vm.name == 'VxRail Manager':
                vxrmIPs.append(vm.summary.guest.ipAddress)
                lenvxrmIPs = len(vxrmIPs)

        containerVM.Destroy()

        if len(vxrmIPs) == 0:
            raise RuntimeError('No VMs VxRail Manager Found in Datacenter: Have they been renamed ?')


        else:
            print(f'### Found a Total of: {lenvxrmIPs} VxRail Manager VMs ###\n')


    except Exception  as err:

        print('Error in findvxrm() :', err)
        sys.exit(1)

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


# Function that takes an argument and calls a set of API based on a list
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


# function to deal with all the different APIs for VXRM
# needs to deal with POST and GET APIs ....
# this is to replace the need for the user to manually write the api name
# For POST requested we will also have to sort out the details
# we also need to take in account the vxrail manager version as not all APIs are available


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
            5. VxRail Upgrade
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
                parameters = {"types": ["vxm", "vcenter", "esxi", "idrac", "ptagent"]}
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
            elif ans == '5':  # POST Implementation
                api = 'lcm/upgrade'
                call = endpoint_url(ip, api)
                method = 'POST'
                parameters = {"bundle_file_locator": "/data/store2/VXRAIL_COMPOSITE-4.7.100-10665885_for_4.7.x.zip",
                              "vxrail": {"vxm_root_user": {"username": "root", "password": "VxR@il1!"}},
                              "vcenter": {
                                  "vc_admin_user": {"username": "administrator@vsphere.local", "password": "VxR@il1!"}}}
                break
            elif ans == '0':
                print('\nExiting Program ...')
                sys.exit(1)
            else:
                print('\n Not Valid Choice Try again')

    except Exception  as err:
        print('Error: ', err)

    return call


# helper function to upload upgrade composite bundle to VxRM
def transfer_bundle(vxrmip=None, file=None, dest='/data/store2'):
    if platform.system() == 'Windows':
        p = subprocess.Popen(['pscp', 'C:\file.txt', 'mystic@172.168.10.150:/tmp'])
        sts = os.waitpid(p.pid, 0)

    return None


def GetArgs():
    """
    Supports the command-line arguments listed below.
    """

    parser = argparse.ArgumentParser(description='Process args for connecting to vCenter')
    parser.add_argument('-v', '--vc', required=True, action='store', help='vCenter')
    parser.add_argument('-u', '--user', required=True, action='store', help='vCenter Administrator')
    parser.add_argument('-p', '--password', required=False, action='store', help='Password')
    args = parser.parse_args()
    return args


# Runs the same API across all the VXRM Identified
# usually for GET methods

def run_same_api(api):
    vxrails = findvxrm()
    for vx in vxrails:
        call_api(url, method)

    return None



def main():
    #    transfer_bundle()

    global content
    global si
    args = GetArgs()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and user %s: ' % (args.vc, args.user))

    try:

        # connection string

        si = connect.SmartConnectNoSSL(host=args.vc,
                                       user=args.user,
                                       pwd=password)

        content = si.RetrieveServiceContent()

        while True:
            global selection
            vx = findvxrm()
            print('Continue ?')
            cont = input('Type Y or N: ')
            if cont == 'Y':
                for vxrm in vx:
                    print(f'VXRM Found with IP: {vxrm}')

                selection = input(
                    'Type the IP of VxRail Manager to Connect to or type "all" to run the same API on ALL VxRail Managers : ')
                if selection in vx:
                    print(vx.index(selection))

                    print('Checking VxRail Manager: ', selection)
                    api = api_list(selection)
                    if api is not None:
                        call_api(api, method)
                    else:
                        break
                elif selection == 'all':
                    print('Put the code here to run the same API on all vxrail managers')
                    vx = findvxrm()  # array with all vxrms
                    for v in vx:
                        api = api_list(
                            v)  # this is not working. need a way to keep the API permanent for that run and just loop over all the nodes ...
                        call_api(api,
                                 method)  # as of now we need to repeat the choice multiple times for every rail. We just want the SAME API to be executed on all rails # function that takes as argument another function ? decorator ???? just to remove the selection part ...
            else:
                print('\nExiting Program ...')
                sys.exit(1)


    except Exception  as err:

        print('Error: ', err)


main()

# Things to improve/implement
# MAJOR FEATURES


# todo - Add an option to run the same API on ALL the VXRM.
# todo - Add support for more APIs

# MINOR FEATURES
# todo - add a function to upload the logs from the VM where the scrip is executed. graphical interface would be fantastic
# todo - close VC connection on program exit
# todo - check power state of vxrm
# todo - Treat exceptions when VXRM have no IP. Ideally IP should come from vSphere
# todo - Get VxRail version Info from VC (4.5 vs 4.7) and Cluster Name. Couldn't find that info in the lab
# todo - progress bar for long return times from POST calls
# fixme test
