#!/usr/bin/python

import sys
import ssl

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

for child in content.rootFolder.childEntity:
    datacenter = child
    vmFolder = datacenter.vmFolder
    vmList = vmFolder.childEntity
    for vm in vmList:
        #        print(vm.name)
        #        print(vm.childEntity)
        name = vm.childEntity
        for x in name:
            print(x.name)
