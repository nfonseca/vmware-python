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

container = content.viewManager.CreateContainerView(content.rootFolder,[],True)
containerVM = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine],True)

print(container)
print(containerVM)
print(containerVM.type)


for obj in containerVM.view:
        print(obj.name)
