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
       print(host)
#by default NETCONF over SSH listens on 830 port, to modify port='22' arg.
#or mode='telnet/console', port='23'

       try:
          with Device(host=host, user='devop', passwd='junOSxp') as dev:
             cu = Config(dev) #like enter to configuration mode
             #diff = cu.diff() #like show |compare command
             #if diff: #Boolean logi true vs false
             cu.rollback(rb_id=1) #If there is a candidate confguration, execute a rollback.
       except ConnectError as err:
           print ("{} Cannot connect to device: {}".format(err, host))
           sys.exit(1)
       except Exception as err:
          print (err)
          sys.exit(1)
