#!/usr/bin/env python3
'''
#Netmiko details:
#++>> cisco IOS, IOS-XR, IOS-XE, IOS-ASA, NX-OS, SG300
#++>> Juniper JunOS
#-->>Arista vEOS
#-->>HP Comware7, ProCurve
#??>>Linux 
#DOC https://github.com/ktbyers/netmiko
#ssh encryptyon error handler at https://unix.stackexchange.com/questions/402746/ssh-unable-to-negotiate-no-matching-key-exchange-method-found
#Python supported versions: 2.7; 3.4; 3.5; 3.6
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
'''
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
#netmiko works with dictionary data structures.
user_login = input('Type a Username: ')
c_passwd = getpass('Type a password for Cisco Devices: ')
with open('inventory.txt') as F:
	device_list = F.read().splitlines()
with open('config_type1.txt') as F:
	config_command1 = F.read().splitlines()
with open('config_type2.txt') as F:
	config_command2 = F.read().splitlines()
with open('config_type3.txt') as F:
	config_command3 = F.read().splitlines()
with open('config_type4.txt') as F:
	config_command4 = F.read().splitlines()	
'''
Rx_ISR_7200 = {
	'device_type': 'cisco_ios',
	'ip': device_list,
	'username': user_login,
	'password': c_passwd,
}

R1_ISR_7200 = {
	'device_type': 'cisco_ios',
	'ip': '192.168.122.11',
	'username': 'devop',
	'password': 'ciscoxp',
}
R2_ISR_7200 = {
	'device_type': 'cisco_ios',
	'ip': '192.168.122.12',
	'username': 'devop',
	'password': 'ciscoxp',
}

R3_ISR_7200 = {
	'device_type': 'cisco_ios',
	'ip': '192.168.122.13',
	'username': 'devop',
	'password': 'ciscoxp',
}	

SW_L3_vIOS = {
	'device_type': 'cisco_ios',
	'ip': '192.168.122.14',
	'username': 'devop',
	'password': 'ciscoxp',

}
devices_list = [R1_ISR_7200, R2_ISR_7200, R3_ISR_7200, SW_L3_vIOS ]
'''
for device in device_list:
    print ("Connecting to device : {ip}".format(ip=device))
    ios_device = {
	    'device_type': 'cisco_ios',
	    'ip': device,
	    'username': user_login,
	    'password': c_passwd,
    }
    try:
        net_connect = ConnectHandler(**ios_device)
    except (AuthenticationException):
        print ('Authentication failure: ' + device)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue
    #Types of devices
    list_versions = ['vios_l2-ADVENTERPRISEK9-M', 
                     'VIOS-ADVENTERPRISEK9-M',
                     'C1900-UNIVERSALK9-M',
                     'C7200-ADVIPSERVICESK9-M'
                     ]

    # Checking the software versions
    for software_ver in list_versions:
        print ('Checking for ' + software_ver)
        output_version = net_connect.send_command('show version')
        int_version = 0 # Reset integer value
        int_version = output_version.find(software_ver) # find() build-in method
        if int_version > 0:
            print ('Software version found: ' + software_ver)
            break
        else:
            print ('Did not find ' + software_ver)

    if software_ver == 'vios_l2-ADVENTERPRISEK9-M':
        print ('Running ' + software_ver + ' commands')
        output = net_connect.send_config_set(config_command1)
        net_connect.disconnect()
    elif software_ver == 'VIOS-ADVENTERPRISEK9-M':
        print ('Running ' + software_ver + ' commands')
        output = net_connect.send_config_set(config_command2)
        net_connect.disconnect()
    elif software_ver == 'C1900-UNIVERSALK9-M':
        print ('Running ' + software_ver + ' commands')
        output = net_connect.send_config_set(config_command3)
        net_connect.disconnect()
    elif software_ver == 'C7200-ADVIPSERVICESK9-M':
        print ('Running ' + software_ver + ' commands')
        output = net_connect.send_config_set(config_command4)
        net_connect.disconnect()    
    print (output)
