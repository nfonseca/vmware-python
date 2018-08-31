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

   parser = argparse.ArgumentParser(description='Process args for connecting to vCenter')
   parser.add_argument('-v', '--vc', required=True, action='store', help='vCenter')
   parser.add_argument('-u', '--user', required=True, action='store', help='vCenter Administrator')
   parser.add_argument('-p', '--password', required=False, action='store', help='Password')
   args = parser.parse_args()

   return args


# can use containerview instead of list view http://rbcollins.net/working-with-vmwares-api-via-python/

# def CreateView():
#
#
#     View = si.ViewManager.CreateListView('vim.ExtensionManager')
#
#     return(View)



def main():

    args = GetArgs()

    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and user %s: ' % (args.vc, args.user))

    try:

        s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        s.verify_mode = ssl.CERT_NONE


        # Connect to Service Instance

        si = connect.SmartConnect(host=args.vc,
                                  user=args.user,
                                  pwd=password,
                                  sslContext=s)


        extmanager = si.content.extensionManager
        print("Type of extmanager is: ")
        print(type(extmanager))
        extview = si.content.viewManager.CreateListView([extmanager])
        print(extview)

        children = extview.view
        for child in children:
            print("In loop")
            print(child.extensionList)






    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0


# Start program
if __name__ == "__main__":
    main()



