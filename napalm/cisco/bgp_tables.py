#!/usr/bin/env python3
import json
from napalm import get_network_driver

def main():
   routers = ['192.168.122.10']
   for router in routers:
       driver = get_network_driver('ios')
       dev = driver(router, 'devop', 'ciscoxp', timeout=10)
       dev.open()

       ios_output = dev.get_bgp_neighbors()
       print ('#' * 60)
       print (json.dumps(ios_output, indent=4)) #data representation is using 4 spaces to delimitation ios_output = 
       print ('#' * 60)
      # ios_output = dev.get_bgp_neighbors_detail() #not supported by IOS
      # print (json.dumps(ios_output, indent=4))
      # print ('#' * 60)
      # ios_output = dev.get_bgp_config() #not supported by IOS
      # print (json.dumps(ios_output, sort_keys=False, indent=4)) #sort_keys=True
      # print ('#' * 60)
       dev.close()

if __name__ == '__main__':
   main()
