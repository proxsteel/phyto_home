#!/usr/bin/env python3
__author__ = 'dotel'
#  (c) 2019, Getting Practice, Inc.
#  Written for JunOS Atomation time
from jnpr.junos import Device
from jnpr.junos.utils.fs import FS
from jnpr.junos.exception import *
from jnpr.junos.utils.config import Config
import multiprocessing
import time
 
NUM_PROCESSES = 4 #the amount of paralel process 1 = serial procesing
DEVICES = "../configs/inventory.txt"
#if DEVICES == None:
#   DEVICES = input("Enter inventory file: ")
with open(DEVICES) as f:
   DEVICE = f.read().splitlines()

def commit_check_rollback(host):
   try:
      with Device(host=host) as dev:
         cu = Config(dev)
         diff = cu.diff()
         print ("On {} device are {} diferencies between acticve and candidate".format(host, diff ))
         if diff:
            cu.rollback()
   except ConnectRefusedError:
      print("{}: Error - Device connection refused!".format(host))
   except ConnectTimeoutError:
      print("%s: Error - Device connection time out!" % host)
   except ConnectAuthError:
      print("%s: Error - Authentication failure!" % host)

def main():
   start_time = time.time()
   with multiprocessing.Pool(processes=NUM_PROCESSES) as process_pool:
      process_pool.map(commit_check_rollback, DEVICE)
      process_pool.close()
      process_pool.join()
   print("Finished in %f sec." % (time.time() - start_time))

#Standard Python script “entry point”.
if __name__ == "__main__":
   main()
