#!/usr/bin/python

import sys

# Site Package Location in VXRM before import module section
sys.path.append("/usr/lib/vmware-marvin/marvind/webapps/ROOT/WEB-INF/classes/scripts/lib/python2.7/site-packages")

import ssl
from pyVmomi import vim, vmodl
from pyVim import connect
from datetime import datetime
import argparse
import getpass


def GetArgs():

   parser = argparse.ArgumentParser(description='Process args for connecting to vCenter')
   parser.add_argument('-v', '--vc', required=True, action='store', help='vCenter')
   parser.add_argument('-u', '--user', required=True, action='store', help='vCenter Administrator')
   parser.add_argument('-p', '--password', required=False, action='store', help='Password')
   args = parser.parse_args()

   return args


# Function to create the View

def get_obj(si):

    extmanager = si.content.extensionManager
    extview = si.content.viewManager.CreateListView([extmanager])
    extview.DestroyView()
    return extview


# Function to create the Filter Spec

# def create_filter_spec(pc, vms, prop):
#     objSpecs = []
#
#     for vm in vms:
#         objSpec = vmodl.query.PropertyCollector.ObjectSpec(obj=vm)
#         objSpecs.append(objSpec)
#
#     filterSpec = vmodl.query.PropertyCollector.FilterSpec()
#     filterSpec.objectSet = objSpecs
#     propSet = vmodl.query.PropertyCollector.PropertySpec(all=False)
#     propSet.type = vim.VirtualMachine
#     propSet.pathSet = [prop]
#     filterSpec.propSet = [propSet]
#     return filterSpec





def main():

# global variables of main

    args = GetArgs()

    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and user %s: ' % (args.vc, args.user))

    try:

        s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        s.verify_mode = ssl.CERT_NONE
        # connection string
        si = connect.SmartConnect(host=args.vc,
                                  user=args.user,
                                  pwd=password,
                                  sslContext=s)

        pc = si.content.propertyCollector

        print(si)




    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0


# Start program
if __name__ == "__main__":
    main()



