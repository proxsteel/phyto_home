#!/usr/bin/env python3

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
#from lxml import etree

with Device(host='192.168.122.199', user='devop', passwd='junOSxp', port=5000, gather_facts=True) as dev:
   cu = Config(dev)
   cu.load(path='/home/backup/mx400-init-config.conf', format='text', merge=True)
   print("Commiting configuration...") 
   cu.commit()

