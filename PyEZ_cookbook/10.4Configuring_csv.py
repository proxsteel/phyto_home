#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
#from lxml import etree
from pprint import pprint
import csv
import time
import os
import sys

USER = "devop"
PW = "junOSxp"
CONFIG_FILE = "config1.txt"

def config_multi_devices(csv_file='config-data.csv'):
    with open(csv_file) as f:
        csvfile = csv.DictReader(f)

        for row in csvfile:
            router = row['router']
            values = {
                'dns_server': row['dns_server'],
                'ntp_server': row['ntp_server'],
                'snmp_location': row['snmp_location'],
                'snmp_contact': row['snmp_contact'],
                'snmp_community': row['snmp_community'],
                'snmp_trap_recvr': row['snmp_trap_recvr']
            }
            try:
               with Device(host=router, user=USER, passwd=PW) as dev:
                  dev.open()
                  print ("{} Connecting to device: {}".format(time.asctime(), router))
                  cu = Config(dev)
                  cu.load(template_path=CONFIG_FILE, template_vars=values, format='set', merge=True)
                  cu.commit(timeout=30)
                  print("{} Committing the configuration on device: {}".format(time.asctime(), router))
                  dev.close()
            except LockError as err:
               print ("{} Cannot lock the candidate config on device: {}".format(time.asctime(), router))
               print("Error message is: {}".format(err))
               pass
            except ConnectError as err:
               print ("{} Cannot connect to device: {}".format(time.asctime(), err))
               pass
            except Exception as err:
               sys.exit(1)

if __name__ == "__main__":
   config_multi_devices()
