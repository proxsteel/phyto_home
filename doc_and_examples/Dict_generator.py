#!/usr/bin/env python3
#from collections import ChainMap

vlan_file = open('vlan.txt', 'r')
vlan_text = vlan_file.read()  #a string obj
vlan_list = vlan_text.splitlines() #a list of elements

vlans = []

for item in vlan_list:
    if 'vlan' in item:
        tmp = {}
#        print(id) 
        id = item.strip()
#        print(id)
        id = id.strip('vlan')
        print(id)
        id = id.strip()
#        print (id)
        tmp['id'] = id
    elif 'name' in item:
        name = item.strip()
        name = name.strip('name')
        name = name.strip()
        print (name)
        tmp['name'] = name
        vlans.append(tmp)
print("a list of dicts: ", vlans)
#d_vlans = {}
#for dect in vlans:
#   d_vlans.update(dect)
#print ("result: ", d_vlans)
#print(d_vlans)
vlan_file.close()
