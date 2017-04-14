from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

#connection string to connect to vCenter

vc = SmartConnect(host="10.27.44.44", user="Administrator@vsphere.local", pwd='VMware123!', sslContext=s)

#Datacenter Level

dc = vc.content.rootFolder.childEntity[0]


# variable that holds the Datastore Specs. this is an array type
datastores = dc.hostFolder.childEntity[0].datastore


#prints all datastores
#we need to make a loop to go over all the indexes

for j in datastores:
    print('Datastore Name:', j.name, 'MOID:', j)



#Inventory Path

path= vc.content.searchIndex.FindByInventoryPath("GSS-VSAN-A/host/Cluster-A/")

print("Looking at Cluster: ",path.name)

for i in path.host:
    print("ESXi FQDN: ",i.name)
    print("Power Management: ", i.hardware.cpuPowerManagementInfo.currentPolicy, '\n')




atexit.register(Disconnect,vc)

