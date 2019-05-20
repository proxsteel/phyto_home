#!/usr/bin/env python3
__author__ = 'dotel'
#  (c) 2019, Getting Practice, Inc.
#  Written for JunOS Atomation time
from jnpr.junos import Device
from jnpr.junos.utils.fs import FS
from jnpr.junos.exception import *
import multiprocessing
import time

NUM_PROCESSES = 5 #number of paralel proccesses
USER = "devop"
PASSWD = "junOSxp"
DEVICES = [
   "192.168.122.10",
   "192.168.122.20",
   "192.168.122.30",
   "192.168.122.40",
   "192.168.122.31",
]

DIRECTORY = "/"

def check_directory_usage(host):
   try:
      with Device(host=host, user=USER, passwd=PASSWD) as dev:
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
      process_pool.map(check_directory_usage, DEVICES)
      process_pool.close()
      process_pool.join()
   print("Finished in %f sec." % (time.time() - start_time))

if __name__ == "__main__":
   main()
