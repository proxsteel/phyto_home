#!/usr/bin/env python3
#  (c) 2019, Getting Practice, Inc.
#  Written for JunOS Atomation time
# Enable NETCONF
#from jnpr.junos import Device
#from jnpr.junos.utils.config import Config
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
import time

#Connection to device and configuration
user_login = input('Username: ')
user_passw = getpass('Password: ') #works like input but gives confidenti.
invent_file = './inventory.txt'

with open(invent_file) as f:
    device_list = f.read().splitlines() #splitlines make a list of lines
#   print (device_list)
    for device in device_list:
        net_device = {
           'device_type': 'juniper',
           'ip': device,
           'username': user_login,
           'password': user_passw,
        }
        print ("{} Connecting to {}".format(time.asctime(), net_device['ip']))
        ssh_connected_dev = ConnectHandler(**net_device)
        configure = ssh_connected_dev.config_mode() #eq edit or configuration mode
        print ("{} Applying configuration to {}".format(time.asctime(), net_device['ip']))
        set_netc_ssh = ssh_connected_dev.send_command("set system services netconf ssh")
        print ("{} Commiting config to {}".format(time.asctime(), net_device['ip']))
#       print (set_netc_ssh)
        ssh_connected_dev.commit(comment='Enable Netconf Service', and_quit=True)
        print ("{} Closing connection to {}".format(time.asctime(), net_device['ip']))
        ssh_connected_dev.disconnect()

