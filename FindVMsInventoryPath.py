from pyVim.connect import SmartConnect
import ssl

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

# connection string

si = SmartConnect(host="10.27.44.44", user="Administrator@vsphere.local", pwd='VMware123!', sslContext=s)

datacenter = si.content.rootFolder.childEntity[0]

vm = si.content.searchIndex.FindByInventoryPath("/")

print(vm)

vms = datacenter.vmFolder.childEntity



