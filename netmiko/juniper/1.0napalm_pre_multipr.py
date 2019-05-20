#!/usr/bin/env python3
import time, sys
from pprint import pprint
from napalm import get_network_driver
from getpass import getpass
from netaddr import *
#from netmiko import ConnectHandler
#from netmiko.ssh_exception import NetMikoTimeoutException
#from netmiko.ssh_exception import NetMikoAuthenticationException
#https://github.com/ksator/junos-automation-with-NAPALM/wiki/How-to-use-NAPALM-with-Python
import multiprocessing

user_login = input('Username: ')
user_passw = getpass('Password: ')
PROC_N = 5

with open('inventory.txt') as f:
     DEVICE = f.read().splitlines()
     for IP in DEVICE:
         if IPAddress(str(IP)).is_unicast():
             DEVICE = DEVICE
         else:
             print ("Wrong IP address: {wr}".format(wr=err))
             sys.exit(1)

#Connection to device and configuration netmiko version
"""def enable_netconf(net_device):
   print ("{} Connecting to {}".format(time.asctime(), net_device['ip']))
   junos_device = ConnectHandler(**net_device)
   configure = junos_device.config_mode() #eq edit or configuration mode
   print ("{} Applying configuration to {}".format(time.asctime(), net_device['ip']))
   set_netc_ssh = junos_device.send_command("set system services netconf ssh")
   print ("{} Commiting config to {}".format(time.asctime(), net_device['ip']))
   junos_device.commit(comment='Enable Netconf Service', and_quit=True)
   print ("{} Closing connection to {}".format(time.asctime(), net_device['ip']))
   junos_device.disconnect()
"""
#Connection to device and configuring: NAPALM version
def enable_netconf(ip):
    try:
        driver = get_network_driver('junos')
        device = driver(ip, user_login, user_passw, timeout=30)
        device.open()
        #output = device.get_facts()
        #pprint (output)
        device.load_merge_candidate(config='set system services netconf ssh') #merge
        #device.load_merge_candidate(config='delete system services netconf ssh')
        #device.load_replace_candidate(filename='new_good.conf')              #replace
        print (device.compare_config())
        #device.discard_config()   #If you are not happy with the changes you can discard them.
        print ("Commiting to device {i}".format(i=ip))
        device.commit_config()
        #device.rollback()         #If for some reason you committed the changes and you want to rollback.
    except Exception as e:
        print(ip, str(e))
    finally:
        device.close()
#Credentials input and passing it to enable_netconf():  netmiko version
"""
def main():
   user_login = input('Username: ')
   user_passw = getpass('Password: ') #works like input but gives confidenti. 
   with open('inventory.txt') as f:
      device_list = f.read().splitlines()
      for device in device_list:
         net_device = {
            'device_type': 'juniper',
            'ip': device,
            'username': user_login,
            'password': user_passw,
         }

         enable_netconf(net_device)
"""
def main():
    start_time = time.time()
    #print(len(DEVICE))
    with multiprocessing.Pool(processes=PROC_N) as process_pool:
        process_pool.map(enable_netconf, DEVICE)
        process_pool.close()
        process_pool.join()
    print("Finished in %f sec." % (time.time() - start_time))

if __name__ == '__main__':
   main() 

