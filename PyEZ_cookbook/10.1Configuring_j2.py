NOTE: incomplete!!!!
#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from lxml import etree
import multiprocessing
import time

#Doesn't work need troubleshooting
USER = "devop"
PASSWD = "junOSxp" 
NUM_PROCESSES = 2
J2_TEMPLET = "../configs/config.txt"
INVENTORY = "../configs/inventory.txt"
MY_VARIABLES = {
             'dns_server': '8.8.8.8',
             'ntp_server': '24.56.178.140',
             'snmp_location': 'DC-1 core rack',
             'snmp_contact': 'NetOps Department',
             'snmp_community': 'netopsrw',
             'snmp_trap_recvr': '192.168.122.1',
}

with open(INVENTORY) as f:
   DEVICE = f.read().splitlines()

def config_dev(host):
   try:
      with Device(host=host, user=USER, passwd=PASSWD) as dev:
         cu = Config(dev)
#         diff = cu.diff()
#         print ("On {} device are {} diferencies between acticve and candidate".format(host, diff ))
#         if diff:
#            cu.rollback()

         cu.load(template_path=J2_TEMPLET, template_vars=MY_VARIABLES, format='set', merge=True)
         cu.commit()
         print("{} Commiting the configuration on device: {}".format(time.asctime(), host))
#      dev.close() 
   except ConnectRefusedError:
      print("{}: Error - Device connection refused!".format(host))
   except ConnectTimeoutError:
      print("%s: Error - Device connection time out!" % host)
   except ConnectAuthError:
      print("%s: Error - Authentication failure!" % host)

def main():
   start_time = time.time()
   with multiprocessing.Pool(processes=NUM_PROCESSES) as process_pool:
      process_pool.map(config_dev, DEVICE)
      process_pool.close() #method to notify the process pool that no other wo$
      process_pool.join()  #method to wait for all the worker processes to fni$
   print("Finished in %f sec." % (time.time() - start_time))

if __name__ == '__main__':
   main()
