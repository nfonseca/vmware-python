from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

#connection string to connect to vCenter

vc = SmartConnect(host="10.27.44.44", user="Administrator@vsphere.local", pwd='VMware123!', sslContext=s)


#Inventory Path

path= vc.content.searchIndex.FindByInventoryPath("GSS-VSAN-A/host/Cluster-A/")

print("Looking at Cluster: ",path.name)

for i in path.host:
    print("ESXi FQDN: ",i.name)
    print("Power Management: ", i.hardware.cpuPowerManagementInfo.currentPolicy, '\n')

# Change the Power Management of the Hosts to Low Power: 3

    i.configManager.powerSystem.ConfigurePowerPolicy(3)

atexit.register(Disconnect,vc)

