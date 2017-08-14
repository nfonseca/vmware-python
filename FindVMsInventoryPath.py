from pyVim.connect import SmartConnect
import ssl

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

# connection string

si = SmartConnect(host="vcsa-gssvsan-b.csl.vmware.com", user="Administrator@vsphere.local", pwd='VMware123!', sslContext=s)

datacenter = si.content.rootFolder.childEntity[0]

root= si.content.rootFolder.childEntity[0]
#print(root)



# loop de todos os child entities e depois ponho dentro dos earch index
# returns all the vm names in the Inventory
dc = si.content.rootFolder.childEntity[0]

for vms in dc.vmFolder.childEntity:

    #print(vms.name)
    vm = si.content.searchIndex.FindByInventoryPath("GSS-VSAN-B/vm/"+vms.name)
    # Root Folder must not be usedvsv
    print(vm.name)







