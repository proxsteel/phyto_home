#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
#from lxml import etree
from pprint import pprint
import multiprocessing
import time
import os
import sys
NUM_PROCESSES = 5 #the amount of paralel process 1 = serial procesing
INVENTORY = "../configs/inventory.txt"
USER = "devop"
PW = "junOSxp"
CONFIG_FILE = 'config1.txt'
MY_VARS = {
        'dns_server': '8.8.8.8',
        'ntp_server': '24.56.178.140',
        'snmp_location': 'Data center core rack',
        'snmp_contact': 'IT Security',
        'snmp_community': 'netopsrw',
        'snmp_trap_recvr': '192.168.122.1'
}
with open(INVENTORY) as f:
   routers = f.read().splitlines() #a list of elemnts == IP asddresses

def config_devices(host):
   try: 
      with Device(host=host, user=USER, passwd=PW) as dev:
         dev.open()
         print ("{} Connecting to device: {}".format(time.asctime(), host))
#        pprint (dev.facts)
         cu = Config(dev) 
         cu.lock() #
         cu.load(template_path=CONFIG_FILE, template_vars=MY_VARS,format='set', merge=True)
#         print (cu.diff())
#         pdiff()
         cu.commit(timeout=30)
         cu.unlock()
         print("{} Commiting the configuration on device: {}".format(time.asctime(), host))
         dev.close()

   except LockError as err:
      print ("{} Cannot lock the candidate config on device: {}".format(time.asctime(), host))
      print("Error message is: {}".format(err))
      pass
   except ConnectError as err:
      print ("Cannot connect to device: {}".format(err))
      pass
   except Exception as err:
      sys.exit(1)

def main():
   start_time = time.time()
   with multiprocessing.Pool(processes=NUM_PROCESSES) as process_pool:
      process_pool.map(config_devices, routers)
      process_pool.close() #method to notify the process pool that no other 
                           #work is going to be submitted to it
      process_pool.join()  #method to wait for all the worker processes to
                           #fnish and terminate
   print("Finished in %f sec." % (time.time() - start_time))

if __name__ == "__main__":
   main()
