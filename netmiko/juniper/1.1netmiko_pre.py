#!/usr/bin/env python3
# Enable NETCONF
import time
#from jnpr.junos import Device
#from jnpr.junos.utils.config import Config
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException


#Connection to device and configuration
def enable_netconf(net_device):
   print ("{} Connecting to {}".format(time.asctime(), net_device['ip']))
   junos_device = ConnectHandler(**net_device)
   configure = junos_device.config_mode() #eq edit or configuration mode
   print ("{} Applying configuration to {}".format(time.asctime(), net_device['ip']))
   set_netc_ssh = junos_device.send_command("delete system services netconf ssh")
   print ("{} Commiting config to {}".format(time.asctime(), net_device['ip']))
   junos_device.commit(comment='Enable Netconf Service', and_quit=True)
   print ("{} Closing connection to {}".format(time.asctime(), net_device['ip']))
   junos_device.disconnect()

#Credentials and device type configuration
def main():
   user_login = input('Username: ')
   user_passw = getpass('Password: ') #works like input but gives confidenti. 
   with open('./inventory.txt') as f:
      device_list = f.read().splitlines()
      for device in device_list:
         net_device = {
            'device_type': 'juniper',
            'ip': device,
            'username': user_login,
            'password': user_passw,
         }

         enable_netconf(net_device)

if __name__ == '__main__':
   main() 

