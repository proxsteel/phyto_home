#!/usr/bin/env python3
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.config import Config
import getpass
import os
import sys
import argparse

inventory = '../configs/inventory.txt'
host = None

if inventory == None:
   inventory = input("Enter inventory file: ")

with open(inventory) as f:
   for line in f:
       host = line.rstrip(os.linesep)
#       print(host)
#by default NETCONF over SSH listens on 830 port, to modify port='22' arg.
#or mode='telnet/console', port='23'
       try:
          with Device(host=host, user="devop", passwd="junOSxp") as dev:
             dev.open()
             print ("Connecting to device: {}".format(host))
             cu = Config(dev)
             cu.rollback(5)
             cu.commit()
             dev.close()
       except ConnectError as err:
           print ("{} Cannot connect to device: {}".format(err, host))
           sys.exit(1)
       except Exception as err:
          print (err)
          sys.exit(1)


       #cu = Config(dev) #like enter to configuration mode 
       #diff = cu.diff() #like show |compare command
       #if diff:
       #cu.rollback() #If there is a candidate confguration, execute a rollback.
#       pprint(dev.facts)
#       dev.close()
