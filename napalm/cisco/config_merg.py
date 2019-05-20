#!/usr/bin/env python3
import json
from napalm import get_network_driver

def main():
   routers = ['192.168.122.11', '192.168.122.12', '192.168.122.13']
  # optional_arg = {'dest_file_system': 'nvram:'}
   for router in routers:
       driver = get_network_driver('ios')
       dev = driver(router, 'devop', 'ciscoxp', timeout=30)
       dev.open()
       print ("Connecting to device {ip}".format(ip=router))
       dev.load_merge_candidate(filename='Prefix_list.cfg')
       diffs = dev.compare_config()
       if len(diffs) > 0:
           print (str(diffs) + \n"The Config has been saved to permanent memory...")
           dev.commit_config()
       else:
           print("No changes detected...\nDiscarding ...")
           dev.discard_config()
      # ios_output = dev.get_bgp_neighbors_detail() #not supported by IOS
      # print (json.dumps(ios_output, indent=4))
      # print ('#' * 60)
      # ios_output = dev.get_bgp_config() #not supported by IOS
      # print (json.dumps(ios_output, sort_keys=False, indent=4)) #sort_keys=True
      # print ('#' * 60)
       dev.close()

if __name__ == '__main__':
   main()
