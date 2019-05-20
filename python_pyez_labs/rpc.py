#!/usr/bin/env python3
# Script to run RPC's using PyEZ.

from jnpr.junos import Device
from lxml import etree


jdev = Device(host='192.168.122.10', user='devop', passwd='junOSxp')

#fitering
filter = '''
            <filter>
                <configuration xmlns="http://xml.juniper.net/xnm!!!
                     <interfaces></interfaces>
                </configuration>
            </filter>
         '''


# Opens a connection with remote device
jdev.open()

# Run rpc
#xml_rsp = jdev.rpc.get_software_information()
print (etree.tostring(jdev.rpc.get_software_information()))
print (etree.tostring(jdev.rpc.get_config(filter_xml='<configuration><interfaces/></configuration>')))
# Close the connection
jdev.close()
