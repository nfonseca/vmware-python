#!/usr/bin/python

import sys
import ssl

# Site Package Location in VXRM
sys.path.append("/usr/lib/vmware-marvin/marvind/webapps/ROOT/WEB-INF/classes/scripts/lib/python2.7/site-packages")
from pyVmomi import vim, vmodl
from pyVim import connect
from datetime import datetime

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

# variables


# connection string

si = connect.SmartConnect(host="192.168.10.10", user="Administrator@vsphere.local", pwd='VMware123$', sslContext=s)

content = si.RetrieveServiceContent()


# using view

rootFolder = si.content.rootFolder
print(rootFolder)
print(rootFolder.name)



#view = si.content.viewManager.CreateContainerView(rootFolder,True)

container = content.viewManager.CreateContainerView(content.rootFolder,[],False)

print(container)


# Create a global view
#
# def get_obj(content, vimtype, name):
#     obj = None
#     container = content.viewManager.CreateContainerView(
#         content.rootFolder, vimtype, True)
#     for c in container.view:
#         if c.name == name:
#             obj = c
#             break
#     return obj


# specs of the script
# 1 - connect to VC
# 2 - Find all Powered ON VMs on the DataCenter (VxRail CLusters Only)
# 3 - Check for every of those VMs if they have an ISO Mounted
# 4 - Report to the user a list of the VMs Found (we can eventually modify the script to remove the ISO)

