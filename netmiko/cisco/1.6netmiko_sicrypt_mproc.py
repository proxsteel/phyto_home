#!/usr/bin/env python3
import time
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
from getpass import getpass
#https://pypi.org/project/simple-crypt/
#examples: https://github.com/andrewcooke/simple-crypt
from simplecrypt import encrypt, decrypt #unlike PyEZ, Netmiko doesn't suport by default ssh 
                                         #user/keys from the host system. this libraly allow the 
                                         #encription of csv files that contains credential data
from pprint import pprint
import csv
import json
#netmiko works with dictionary data structures.

def read_devices( devices_filename ):
    '''A simple function that reads data from CVS file and is conveting it into a dictionary
       By iterating and building a list of elements'''
    devices = {}  # create our dictionary for storing devices and their info

    with open( devices_filename ) as devices_file:

        for device_line in devices_file:

            device_info = device_line.strip().split(',')  #extract device info from line
            #-----a print for debugging
            print(device_info, type(device_info))
            device = {'ipaddr': device_info[0],
                      'type':   device_info[1],
                      'name':   device_info[2]}  # create dictionary of device objects ...

            devices[device['ipaddr']] = device  # store our device in the devices dictionary
                                                # note the key for devices dictionary entries 
                                                # is ipaddr

    print ('\n----- devices in dictonary format----------------------')
    pprint( devices )

    return devices

def read_device_creds(encrypted_cerds_filename, KEY):
    '''A function hat read credentials and decrypt from an ecrypted file. Passed arguments are:
       read_device_creds(file, password)'''
    print("\n***Loading credentials from the encrypted file ...\n")
    #----encrypt() the cerdential file
    with open( encrypted_cerds_filename, 'rb') as device_creds_file:
        device_creds_json = decrypt(KEY, device_creds_file.read())
    #----Print the a list of lists from decripted file
    device_creds_list = json.loads( device_creds_json.decode('utf-8'))
    #----for debugging
    #for dev in device_creds_list:
    #    print ("TEST", {dev[0]:dev})
    pprint( device_creds_list, type(device_creds_list) )
    print ('\n----- confirm: device_creds in json format--------------------------')
    # converting to a dictionary of lists using dictionary's  
    device_creds = { dev[0]:dev for dev in device_creds_list }
    #----for debugging
    pprint( device_creds )
    
    return device_creds

def config_worker( device, creds ):

    #---- Connect to the device ----
    if   device['type'] == 'junos-srx': device_type = 'juniper'
    elif device['type'] == 'cisco-ios': device_type = 'cisco_ios'
    elif device['type'] == 'cisco-xr':  device_type = 'cisco_xr'
    else:                               device_type = 'cisco_ios'    # attempt Cisco IOS as default

    print ('---- Connecting to device {d}, username={u}, password={p}'.format( d=device['ipaddr'],
                                                                            u=creds[1], p=creds[2] ))

    #---- Connect to the device
    session = ConnectHandler( device_type=device_type, ip=device['ipaddr'],
                                                       username=creds[1], password=creds[2] )
    #session = ConnectHandler( device_type=device_type, ip='172.16.0.1',  # Faking out IP address for now
    #                                                   username=creds[1], password=creds[2] )

    if device_type == 'juniper':
        #---- Use CLI command to get configuration data from device
        print ('---- Getting configuration from device')
        session.send_command('configure terminal')
        config_data = session.send_command('show configuration')

    if device_type == 'cisco_ios':
        #---- Use CLI command to get configuration data from device
        print ('---- Getting configuration from device')
        config_data = session.send_command('show run')
   

    if device_type == 'cisco_xr':
        #---- Use CLI command to get configuration data from device
        print ('---- Getting configuration from device')
        config_data = session.send_command('show configuration running-config')
   
    #---- Write out configuration information to file
    config_filename = 'config-' + device['ipaddr']  # Important - create unique configuration file name

    print ('---- Writing configuration: ', config_filename)
    with open( config_filename, 'w' ) as config_out:  config_out.write( config_data )

    session.disconnect()

    #return ("Saved!")

#==============================================================================
# ---- Main: Get Configuration
#==============================================================================

devices = read_devices( 'inventory_CSV.txt' )
creds   = read_device_creds( 'encrypted_inventory_creds', 'big53cr3t' )

starting_time = time.time()

print ('\n---- Begin get config sequential ------\n')
for ipaddr,device in devices.items():

    print ('Getting config for: ', device)
    config_worker( device, creds[ipaddr] )

print ('\n---- End get config sequential, elapsed time=', time.time()-starting_time) 
