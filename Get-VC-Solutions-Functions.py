#!/usr/bin/python

import sys
import ssl
from pyVmomi import vim, vmodl
from pyVim import connect
from datetime import datetime
import argparse
import getpass

# Site Package Location in VXRM
sys.path.append("/usr/lib/vmware-marvin/marvind/webapps/ROOT/WEB-INF/classes/scripts/lib/python2.7/site-packages")

def GetArgs():

   parser = argparse.ArgumentParser(description='Process args for connecting to vCenter')
   parser.add_argument('-v', '--vc', required=True, action='store', help='vCenter')
   parser.add_argument('-u', '--user', required=True, action='store', help='vCenter Administrator')
   parser.add_argument('-p', '--password', required=False, action='store', help='Password')
   args = parser.parse_args()

   return args


# can use containerview instead of list view http://rbcollins.net/working-with-vmwares-api-via-python/

# def CreateView():
#
#
#     View = si.ViewManager.CreateListView('vim.ExtensionManager')
#
#     return(View)



def main():

    args = GetArgs()

    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and user %s: ' % (args.vc, args.user))

    try:

        s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        s.verify_mode = ssl.CERT_NONE


        # Connect to Service Instance

        si = connect.SmartConnect(host=args.vc,
                                  user=args.user,
                                  pwd=password,
                                  sslContext=s)

        # STEP3: Create a TraversalSpec

        # Implementation seems OK
        travType = vim.view.View
        print(travType)
        print(type(travType))
        travSpec = vmodl.query.PropertyCollector.TraversalSpec(
            name="travSpec for the View",
            path="company",
            skip=False,
            type=vim.view.View)

        print("Printing travSpec.....")
        print(travSpec)

# STEP1: View Creation

        extmanager = si.content.extensionManager
        print("Type of extmanager is: ")
        print(type(extmanager))
        extview = si.content.viewManager.CreateListView([extmanager]) # create a ListView where obj is Extension Manager
        print(extview)

        children = extview.view #assigne the property view to a new variable (object ?)
        for child in children:
            print("In loop")
            print(child.extensionList) # go through all the children attributes on the list


# STEP2:  BUILDING THE FILTERSPEC
# need to find a way to selectively collect only the properties I am interested in . Property Collector ?!?!?!?!?

        # this seems implemented OK
        objSpec = vmodl.Query.PropertyCollector.ObjectSpec(
                obj=extview,
                skip=False,
                selectSet=[travSpec])
        print("Printing objSpec")
        print(objSpec)

        propSpec = vmodl.Query.PropertyCollector.PropertySpec( #use vim.extensionManager
                type=vim.extensionManager,
                all=False,
                pathSet=["company"])
        print("Printing propSpec")
        print(propSpec)

        filterSpec = vmodl.Query.PropertyCollector.FilterSpec(
                propSet=[propSpec],
                objectSet=[objSpec],
                reportMissingObjectsInResults=False)

        print("==>FilterSpec to be used")
        print(filterSpec)

            # creating the filter
        print("==>Filter to be used")
        task_filter = vmodl.query.PropertyCollector.Filter(filterSpec, True)
        print(task_filter)

        # Retrieve properties
        retOptions = vim.PropertyCollector.RetrieveOptions()
        print(retOptions)
        props = si.content.propertyCollector.RetrievePropertiesEx(specSet=[filterSpec],options=retOptions)
        print("Printing PROPS")
        print(props)

#        data = []
#        for obj in props:
#            properties = {}
#            for prop in obj.propSet:
#                properties[prop.name] = prop.val

#            data.append(properties)
#            print(data)


    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0


# Start program
if __name__ == "__main__":
    main()



