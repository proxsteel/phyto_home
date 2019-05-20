#!/usr/bin/env python3
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
from netmiko import ConnectHandler

#netmiko works with dictionary data structures.
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
devices = [R1_ISR_7200, R2_ISR_7200, R3_ISR_7200 ]

for device in devices:
    net_connect = ConnectHandler(**device)
    cli_output = net_connect.send_command('show ip interface brief | inc up | exc unassigned')
    print(cli_output)
    config_command = ['interface fa 0/0', 'description -=To MGMT Station', 'no shutdown']
    cli_input = net_connect.send_config_set(config_command)
    print(cli_input)
#    print ("1st: ", net_connect.check_config_mode())
    write_memory = ['do wr']
    std_out = net_connect.send_config_set(write_memory)
    print ("Saving configuration: {}".format(std_out))
#    print ("2nd: ", net_connect.check_config_mode())
    print ("Disconnecting from device : {ip}".format(ip=device['ip']))
    net_connect.disconnect()
