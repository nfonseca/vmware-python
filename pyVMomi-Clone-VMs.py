from pyVim.connect import SmartConnect
import ssl

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

# connection string

vc = SmartConnect(host="10.27.44.44", user="Administrator@vsphere.local", pwd='VMware123!', sslContext=s)



datacenter = vc.content.rootFolder.childEntity[0]
vms = datacenter.vmFolder.childEntity
dc = vc.content.rootFolder.childEntity[0]
print(dc.name)
print(dc.hostFolder.childEntity[0])

#variable that holds the Datastore Specs
datastores = dc.hostFolder.childEntity[0].datastore
#print("DATASTORE CALL", datastores.datastore)
#ds=datastores.datastore

#prints all datastores
#we need to make a loop to go over all the indexes

for j in datastores:
    print(j.name)


for i in vms:
    print(i.name)
#    print(vc.CurrentTime())


# vmRef =
# vmFolderRef =
# clonedName =
# cloneSpec =
#
#
# clone = vc.service.cloneVM_Task(vmRef, vmFolderRef, clonedName, cloneSpec)

