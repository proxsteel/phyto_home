#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
#from lxml import etree
from pprint import pprint
import time
import os
import sys
#Doesn't work need troubleshooting

USER = "devop"
PW = "junOSxp"
CONFIG_FILE = 'config1.txt'
MY_VARS = {
	'dns_server': '8.8.8.8',
	'ntp_server': '24.56.178.140',
	'snmp_location': 'Data center core rack',
	'snmp_contact': 'IT Security',
	'snmp_community': 'netopsrw',
	'snmp_trap_recvr': '192.168.122.1'
}
def config_devices(INVENTORY="../configs/inventory.txt"):
   try:
      with open(INVENTORY, 'r') as f:
         routers = f.readlines()
         routers = [x.strip() for x in routers]

         for ROUTER in routers:
            dev = Device(host=ROUTER, user=USER, passwd=PW).open()
            print ("{} Connecting to device: {}".format(time.asctime(), ROUTER))
#        pprint (dev.facts)
            try:
               with Config(dev) as cu:
                  cu.lock() #
                  cu.load(template_path=CONFIG_FILE, template_vars=MY_VARS,format='set', merge=True)
#                  print (cu.diff())
#                  pdiff()
                  cu.commit(timeout=30)
                  cu.unlock()
                  print("{} Commiting the configuration on device: {}".format(time.asctime(), ROUTER))
            except LockError as err:
               print ("{} Cannot lock the candidate config on device: {}".format(time.asctime(), ROUTER))
               print("Error message is: {}".format(err))
               sys.exit(1)
   except ConnectError as err:
      print ("Cannot connect to device: {}".format(err))
      sys.exit(1)
   except Exception as err:
      print (err)
      sys.exit(1)
      dev.close()

if __name__ == "__main__":
   config_devices()
