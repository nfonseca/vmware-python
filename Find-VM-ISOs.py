#!/usr/bin/python

# we use sys.path to add the location of the extra modules required

sys.path.append("/usr/lib/vmware-marvin/marvind/webapps/ROOT/WEB-INF/classes/scripts/lib/python2.7/site-packages")
from pyVmomi import vim, vmodl
from pyVim import connect
from datetime import datetime

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

# connection string

si = SmartConnect(host="vcsa-gssvsan-b.csl.vmware.com", user="Administrator@vsphere.local", pwd='VMware123!', sslContext=s)




dcs = si.content.rootFolder.childEntity

# loop over all Datacenters and retrieve all VM's
for dc in dcs:

    print(dc.name)

    for vms in dc.vmFolder.childEntity:

        vm = si.content.searchIndex.FindByInventoryPath(dc.name+"/vm/"+vms.name)
        print("Datacenter:"+dc.name+ " " +"VM:"+ vm.name)