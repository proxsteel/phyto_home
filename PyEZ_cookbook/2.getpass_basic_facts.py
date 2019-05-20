#!/usr/bin/env python3
from pprint import pprint
from jnpr.junos import Device
import getpass

host = None
user = None
pw = None

if host == None:
   host = input("Hostname or IP: ")
if user == None:
   user = input("Username: ")
#if pw == None:
#   pw = input("Password: ")
if pw == None:
   pw = getpass.getpass()	

#by default NETCONF over SSH listens on 830 port, to modify it use port='22' arg.
# Telnet connection
#dev = Device(host=hostname, user=username, passwd=password, mode='telnet',port='23')
# Serial console connection
#dev = Device(host=hostname, user=username, passwd=password, mode='serial',port='/dev/ttyUSB0')

dev = Device(host=host, user=user, passwd=pw)
dev.open()
pprint(dev.facts)

dev.close()
