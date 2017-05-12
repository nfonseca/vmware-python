from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import Cache
import ssl
import atexit
# import the VSAN API python bindings

#import the vSAN API python bindings

import vsanmgmtObjects
import vsanapiutils

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

# connection string to connect to vCenter

sc = SmartConnect(host='10.27.44.44', user='Administrator@vsphere.local', pwd='VMware123!', sslContext=s)

# Datacenter Level

dc = sc.content.rootFolder.childEntity[0]





# Find by Child Method to retrive hosts
# retrieves all the hosts from the DC

hosts = sc.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host

for h in  hosts:

    print(h.name)
    print(h.configManager.advancedOption.setting)





# Close the VCenter Connection

atexit.register(Disconnect, sc)
