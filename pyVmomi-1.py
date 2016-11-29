from pyVim.connect import SmartConnect
import ssl

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

c = SmartConnect(host="10.27.44.44", user="Administrator@vsphere.local", pwd='VMware123!', sslContext=s)

#print(c.CurrentTime())

datacenter = c.content.rootFolder.childEntity[0]
vms = datacenter.vmFolder.childEntity

for i in vms:
    print(i.name)

