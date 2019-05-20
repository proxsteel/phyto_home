#!/usr/bin/env python3

from jnpr.junos import Device
from lxml import etree

print ("Terminal Server Inventory Report")

count = 5000 #set a variable that starts within port range on the terminal server
#host IP is the terminal's server IP and the port is the forwarded one...
while count < 5010:
   try:
      with Device(host='192.168.122.199', user='devop', passwd='junOSxp', mode='telnet', port=count, gather_facts=True) as dev:
         dev_info = dev.facts
         print ('Hostname:' + dev_info['hostname'] + ',' + 'Hardware:' + dev_info['model'] + ',' + 'Software:' + dev_info['version'] + ',' + 'TerminalPort:' + str(count))
   except:
      pass
   count += 1
