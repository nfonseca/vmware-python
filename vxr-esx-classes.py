#!/usr/bin/python


# !/usr/bin/python

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
    parser.add_argument('-v', '--vc', required=True, action='store', help='vCenter')
    parser.add_argument('-u', '--user', required=True, action='store', help='vCenter Administrator')
    parser.add_argument('-p', '--password', required=False, action='store', help='Password')
    args = parser.parse_args()
    return args


class VxrailHost(object):
    """A class that defines ESX attributes for a VxRail Host

    Attributes:
        esxversion: Version of ESXi
        marvinvib: Version of the Marvin vib.
    """

    def __init__(self, esxversion):
        """Return a esx version."""
        self.esxversion = esxversion

    def GetEsxVersion(self, host):
        """Returns the ESXi version from VC"""
        version = vim.HostSystem.config.product.fullName
        return self.version


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
        viewType = [vim.HostSystem]  # object types to look for, Hosts in this case
        recursive = True  # whether we should look into it recursively
        containerView = content.viewManager.CreateContainerView(container,
                                                                viewType,
                                                                recursive)

        children = containerView.view
        for child in children:
            child.GetEsxVersion(child)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0


# Start program
if __name__ == "__main__":
    main()
