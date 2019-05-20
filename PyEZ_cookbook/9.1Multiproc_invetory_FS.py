#!/usr/bin/env python3
__author__ = 'dotel'
#  (c) 2019, Getting Practice, Inc.
#  Written for JunOS Atomation time
from jnpr.junos import Device
from jnpr.junos.utils.fs import FS
from jnpr.junos.exception import *
from getpass import getpass
import multiprocessing
import time
import os
import sys 
NUM_PROCESSES = 1 #number of paralel proccesses
DIRECTORY = "/var/log"
DEVICES = "../configs/inventory.txt"
#USER = "dotel"
#PASSWD = "*****"#based on PyEZ's Device() using SSH key-based authentication  
#DEVICES =  [
#   "192.168.122.10",
#   "192.168.122.20",
#]
#DIRECTORY = "/var/tmp"
with open(DEVICES) as f:
   DEVICE = f.read().splitlines()


def check_directory_usage(host):
   try:
      with Device(host=host) as dev:
         fs = FS(dev)
         print("Checking %s:" %host, end="")
         #print("Checking {}:".format{host}, end="")
         print(fs.directory_usage(DIRECTORY))
   except ConnectRefusedError:
      print("{}: Error - Device connection refused!".format(host))
   except ConnectTimeoutError:
      print("%s: Error - Device connection time out!" % host)
   except ConnectAuthError:
      print("%s: Error - Authentication failure!" % host)

def main():
   start_time = time.time()
   with multiprocessing.Pool(processes=NUM_PROCESSES) as process_pool:
      process_pool.map(check_directory_usage, DEVICE)
      process_pool.close()
      process_pool.join()
   print("Finished in %f sec." % (time.time() - start_time))

if __name__ == "__main__":
   main()
