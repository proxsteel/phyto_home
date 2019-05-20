#!/usr/bin/env python3
#doesn't work !!!!
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
#from lxml import etree
#from pprint import pprint
import multiprocessing
import csv
import time
import os
import sys
NUM_PROCESSES = 1
USER = "devop"
PW = "junOSxp"
CONFIG_FILE = "config1.txt"
csv_file='config-data.csv'

with open(csv_file) as f:
    csvfile = csv.DictReader(f)
    csvfileR = csv.reader(f)
    fields = csvfileR.next()
    print (fields)
    for row in csvfileR:
        ROUTER = (row['router'])
        #print (type(ROUTER))
        VALUES = {
            'dns_server': row['dns_server'],
            'ntp_server': row['ntp_server'],
            'snmp_location': row['snmp_location'],
            'snmp_contact': row['snmp_contact'],
            'snmp_community': row['snmp_community'],
            'snmp_trap_recvr': row['snmp_trap_recvr']
        }
#        print (ROUTER)

def config_devices(host):
   print (host)
   try:
       with Device(host=host, user=USER, passwd=PW) as dev:
          dev.open()
          print ("{} Connecting to device: {}".format(time.asctime(), host))
          cu = Config(dev)
          cu.lock()
          cu.load(template_path=CONFIG_FILE, template_vars=VALUES, format='set', merge=True)
          cu.commit(timeout=30)
          cu.unlock()
          print("{} Committing the configuration on device: {}".format(time.asctime(), host))
          dev.close()

   except LockError as err:
      print ("{} Cannot lock the candidate config on device: {}".format(time.asctime(), host))
      print("Error message is: {}".format(err))
      pass
   except ConnectError as err:
      print ("{} Cannot connect to device: {}".format(time.asctime(), err))
      pass
   except Exception as err:
      sys.exit(1)

def main():
    start_time = time.time()
    with multiprocessing.Pool(processes=NUM_PROCESSES) as process_pool:
       process_pool.map(config_devices, list(ROUTER)) #needs a list not a string as provide the top loop
       process_pool.close()
       process_pool.join()
    print ("Finished in {} sec.".format(time.time() - start_time))

if __name__ == "__main__":
   main()
