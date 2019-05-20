#!/usr/bin/env python3
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
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
          with Device(host=host) as dev:
             pprint (dev.facts)
       except ConnectError as err:
           print ("Cannot connect to device: {0}".format(err))
           sys.exit(1)
       except Exception as err:
          print (err)
          sys.exit(1)

