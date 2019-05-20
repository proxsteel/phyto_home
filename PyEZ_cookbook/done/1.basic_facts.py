#!/usr/bin/env python3
from pprint import pprint
from jnpr.junos import Device

#by default NETCONF over SSH listens on 830 port, to modify port='22' arg.

dev = Device(host='192.168.122.10', user='dotel', passwd='junOSxp', port='22')
dev.open()
pprint(dev.facts)

dev.close()
