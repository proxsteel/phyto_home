#!/usr/bin/env python3
# Copy of Copyright Juniper Networks
# All rights reserved to edit and modify.
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

USER = "devop"
PW = "junOSxp"
CONFIG_FILE = 'config1.txt'
CONFIG_DATA = {
        'dns_server': '8.8.8.8',
        'ntp_server': '24.56.178.140',
        'snmp_location': 'Data center core rack',
        'snmp_contact': 'IT Security',
        'snmp_community': 'snmprw',
        'snmp_trap_recvr': '192.168.1.10'
}

def config_devices(devices="../configs/inventory.txt"):
   with open(devices, 'r') as f:
      firewalls = f.readlines() #a liat of elements + whitespace or new line
      firewalls = [x.strip() for x in firewalls] #strip \n or whitespaces
      print (firewalls)
      for firewall in firewalls:
         dev = Device(host=firewall, user=USER, passwd=PW).open()
         with Config(dev) as cu:
             cu.load(template_path=CONFIG_FILE, template_vars=CONFIG_DATA, format='set', merge=True)
             cu.commit(timeout=30)
             print("Committing the configuration on device: {}".format(firewall))
         dev.close()

if __name__ == "__main__":
   config_devices()
