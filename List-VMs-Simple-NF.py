#!/usr/bin/python

import sys
import ssl

# Site Package Location in VXRM
sys.path.append("/usr/lib/vmware-marvin/marvind/webapps/ROOT/WEB-INF/classes/scripts/lib/python2.7/site-packages")
from pyVmomi import vim, vmodl
from pyVim import connect
from datetime import datetime
import argparse
import getpass

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """

   parser = argparse.ArgumentParser(description='Process args for connecting to vCenter')
   parser.add_argument('-v', '--vc', required=True, action='store', help='vCenter IP to connect to')
   parser.add_argument('-u', '--user', required=True, action='store', help='vCenter Administrator')
   parser.add_argument('-p', '--password', required=False, action='store', help='Password')
   args = parser.parse_args()
   return args


def print_vm_info(virtual_machine):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    config = virtual_machine.config
    print("Name       : ", config.name)
    print("Template   : ", config.template)
    print("Guest      : ", config.guestFullName)
    print("Instance UUID : ", config.instanceUuid)
    print("Bios UUID     : ", config.uuid)
    print("")


def has_iso(virtual_machine):

    iso_path = virtual_machine.config.hardware.device

    for devices in  iso_path:
        if isinstance(devices,vim.vm.device.VirtualCdrom):
                print(devices.backing)


def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """

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

        content = si.RetrieveServiceContent()


        container = content.rootFolder  # starting point to look into
        viewType = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        containerView = content.viewManager.CreateContainerView(container,
                                                                viewType,
                                                                recursive)

        children = containerView.view
        for child in children:
#            print_vm_info(child)
            has_iso(child)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0

# Start program
if __name__ == "__main__":
    main()
