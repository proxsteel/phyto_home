#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.exception import *
from pprint import pprint
import sys
import re
import os
import time

# step 1.1
def main():
    """Simple main method to enter log entries."""
    ROUTERS = ['192.168.122.10', '192.168.122.20', '192.168.122.30', '192.168.122.40']
    op_user = 'devop'
    op_pass = 'junOSxp'
#step 1.3 coment all print statements and use compile() method to create a regex to extract the link down messages
#step 1.3 finditer() method to retrive all matching log messages
#original REGEX: ('(\w{1,3}\s{1,3}\d{1,2}\s{1,3}\d{1,2}:\d{1,2}:\d{1,2}).*SNMP_TRAP_LINK_DOWN.*ifName ([gax]e-\d{1,2}\/\d{1,2})\n')
#https://www.regextester.com/
    link_down = re.compile('(\w{1,3}\s{1,3}\d{1,2}\s{1,3}\d{1,2}:\d{1,2}:\d{1,2}).*SNMP_TRAP_LINK_DOWN.*ifName (em[0-9])')
    for router in ROUTERS:
        try:
            device = Device(host=router, user=op_user, passwd=op_pass)
            print ('Connecting to device {r}'.format(r=router))
            device.open()
            #pprint (device.facts)
# step 1.2 coment pprint statment
            logs = device.rpc.get_log(filename='messages')
            for log_content in logs.iter("file-content"):
                #print (type(log_content))
                #print (dir(log_content))
                #print (log_content.text)
                messages = link_down.finditer(log_content.text)
                # step1.3
                for log in messages:
                    #step 1.3
                    #print(log.group(0))
                    #print(log)
                    #step 1.4
                    #group() method: 1 is the first () in compile() and 2 is the second
                    #group 0 is the entire message that match
                    print("Starting DownTime: ", log.group(1))
                    print("Interface Name: ", log.group(2))
                    #print(log.group(0))
            device.close()
        except Exception as e:
            print ("We have a problem retrieving the information")
            print ('Here is the error {error}'.format(error=e))

if __name__ == "__main__":
    sys.exit(main())
