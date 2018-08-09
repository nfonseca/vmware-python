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


traversal = vmodl.query.PropertyCollector.TraversalSpec(name='VMs', type=vim.VirtualMachine, path="vm",skip=False)
print(traversal)

#object_spec = vmodl.query.PropertyCollector.ObjectSpec(containerVM,traversal,True)


#spec = vmodl.query.PropertyCollector.FilterSpec(containerVM,traversal,True)


#filter = si.content.propertyCollector.CreateFilter(spec,partialUpdates)



# data object for the filter

data = vmodl.query.PropertyCollector.ObjectSpec()

#populate

data.obj =containerVM
data.selectSet = []
data.skip=True



# start populating the instantiated object

data_object_filter=vmodl.query.PropertyCollector.PropertySpec()
data_object_filter.type=vim.VirtualMachine
data_object_filter.all= True
data_object_filter.pathSet = []

print(data_object_filter)

#propertyFilter.propSet =  data_object_filter

#propertyFilter.objectSet = []


# instance an empty object for the Filter Spec
#propertyFilter = vmodl.query.PropertyCollector.FilterSpec()


for obj in containerVM.view:
        print(obj.name)
