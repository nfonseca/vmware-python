from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import Cache
import ssl
import atexit
from pyVmomi import vim
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

print(hosts)
print(hosts[0])

print(hosts[0].configManager.advancedOption)

advsetting = hosts[0].configManager.advancedOption.setting

# setting is type array

# Loop over all the settings and look for vSAN CLomd Repair Time





for i in advsetting:

    if i.key == "VSAN.ClomRepairDelay":

        print(i.key)
        print(i.value)
        print(sc.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0].configManager.advancedOption.QueryOptions('VSAN.ClomRepairDelay'))
        repair = sc.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0].configManager.advancedOption.QueryOptions('VSAN.ClomRepairDelay')

        changedValue = repair[0]
        changedValue.key = 'VSAN.ClomRepairDelay'
        changedValue.value = '120'
        bn = vim.option.OptionValue(key='VSAN.ClomRepairDelay', value=120)
        print(bn)


# creio que tenho erro devido a estar dentro do loop
#        TypeError: 'vim.option.OptionValue'
#        object is not iterable
# rever isto

        sc.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0].configManager.advancedOption.UpdateOptions(bn)



atexit.register(Disconnect, sc)
