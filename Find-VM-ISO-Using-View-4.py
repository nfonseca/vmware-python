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


# We create a container View for all the VMs


containerVM = content.viewManager.CreateContainerView(content.rootFolder,[vim.VirtualMachine],True)


# we check now the container content

# 'vim.view.ContainerView:session[5250eaf3-5813-5f70-a648-0bd716191c66]52708a00-cdc6-4b56-db9f-3ccf0c8f9512'
# the container
print(containerVM)


for obj in containerVM.view:
        print(obj.name)


traversal_spec = vmodl.query.PropertyCollector.TraversalSpec(name='VMs', type=vim.VirtualMachine, path="vm",skip=False)



objSpec = vmodl.Query.PropertyCollector.ObjectSpec(
obj = containerVM,
skip = False,
selectSet = [])

propSpec = vmodl.Query.PropertyCollector.PropertySpec(
type = vim.VirtualMachine,
all = False,
pathSet = ["name"])

filterSpec = vmodl.Query.PropertyCollector.FilterSpec(
propSet = [propSpec],
objectSet = [objSpec])

filter = content.propertyCollector.CreateFilter(filterSpec, False)
