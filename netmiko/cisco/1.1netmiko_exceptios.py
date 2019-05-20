#!/usr/bin/env python3
#
#net_connect.send_command()
#net_connect.config_mode() -- Enter into config mode
#net_connect.check_config_mode() -- Check if you are in config mode, return a boolean
#net_connect.exit_config_mode() -- Exit config mode
#net_connect.clear_buffer() -- Clear the output buffer on the remote device
#net_connect.enable() -- Enter enable mode
#net_connect.exit_enable_mode() -- Exit enable mode
#net_connect.find_prompt() -- Return the current router prompt
#net_connect.commit(arguments) -- Execute a commit action on Juniper and IOS-XR
#net_connect.disconnect() -- Close the SSH connection
#net_connect.send_command(arguments) -- Send command down the SSH channel, return output back
#net_connect.send_config_set(arguments) -- Send a set of configuration commands to remote device
#net_connect.send_config_from_file(arguments) -- Send a set of configuration commands loaded from a file
#
import time, sys
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko import SSHException

#netmiko works with dictionary data structures.
def config_dev(net_device):
   try:
       net_connect = ConnectHandler(**net_device)
       std_input = net_connect.send_command('show ip interface brief | inc up | exc unassigned')
       print("Show command output: ", std_input)
       config_command = ['interface fa 0/0', 'description -=To NMS HUB=-', 'no shutdown', '\n', 'do wr', '\n']
       std_out = net_connect.send_config_set(config_command)
       print(std_out)
       print ("{t} Configuration has been saved on device: {nd}".format(t=time.asctime(), nd=net_device['ip']))

   except NetMikoAuthenticationException as err:
       print ("{t} -=E1=- {e}".format(t=time.asctime(), e=err))
   except NetMikoTimeoutException as err:
       print ("{t} -=E2=- {e}".format(t=time.asctime(), e=err))
       pass
   except (EOFError, SSHException) as err:
       print ("{t} -=E3=- {e}".format(t=time.asctime(), e=err))
   except Exception as err:
       print ("{t} An exception occured: {ex}".format(t=time.asctime(), ex=err))
       sys.exit()
   if not net_connect:
        print ("{t} Disconnecting from device : {nd}".format(t=time.asctime(), nd=net_device['ip']))
        net_connect.disconnect()

#Credentials and device type configuration
def main():
   user_login = input('Username: ')
   user_passw = getpass('Password: ') #works like input but gives confidenti.
   with open('./inventory.txt') as f:
      device_list = f.read().splitlines()
      for device in device_list:
         net_device = {
            'device_type': 'cisco_ios',
            'ip': device,
            'username': user_login,
            'password': user_passw,
         }

         config_dev(net_device)

if __name__ == '__main__':
   main()

