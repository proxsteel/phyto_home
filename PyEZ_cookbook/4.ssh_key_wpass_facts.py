#!/usr/bin/env python3
from pprint import pprint
from jnpr.junos import Device
import getpass

host = None
uname = None #with passfrase
pw = None   #with passphrase
key_file = '/home/dotel/.ssh/id_rsa_a.pub'
#for this key user dotel pw junOSxp id_rsa.pub hasn't a passphrase

if host == None:
   host = input("Hostname or IP: ")
if uname == None:
   uname = input("Username: ")
if pw == None:
   pw = getpass.getpass("SSH passphrase: ")


#by default NETCONF over SSH listens on 830 port, to modify it use port='22' arg.
# Telnet connection
#dev = Device(host=hostname, user=username, passwd=password, mode='telnet',port='23')
# Serial console connection
#dev = Device(host=hostname, user=username, passwd=password, mode='serial',port='/dev/ttyUSB0')

dev = Device(host=host, user=uname, passwd=pw, ssh_private_key_file=key_file)


dev.open()
pprint(dev.facts)

dev.close()
