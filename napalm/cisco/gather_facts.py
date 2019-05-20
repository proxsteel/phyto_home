#!/usr/bin/env python3
import json
from napalm import get_network_driver
driver = get_network_driver('ios')
l2dev = driver('192.168.122.11', 'devop', 'ciscoxp')
l2dev.open()

ios_output = l2dev.get_facts()
print ('#' * 60)
print (json.dumps(ios_output, indent=4)) #data representation is using 4 spaces to delimitation ios_output = 
print ('#' * 60)
ios_output = l2dev.get_interfaces()
print (json.dumps(ios_output, indent=4))
print ('#' * 60)
ios_output = l2dev.get_interfaces_counters()
print (json.dumps(ios_output, sort_keys=False, indent=4)) #sort_keys=True
print ('#' * 60)
