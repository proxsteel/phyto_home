#!/usr/bin/env python3
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
#CSV file is inventory_creds.txt

#---- Read in pertinent information from user
row_cerds_filename = input('\nInput CSV filename :  ') or 'inventory_creds.txt'
KEY                = getpass('Encryption key: ')

#---- Read in the device credentials from CSV file into list of device credentials
with open( row_cerds_filename, 'r' ) as dc_in:
    device_creds_reader = csv.reader( dc_in )
    #from csv file creating a list of lists that contains device details...
    device_creds_list = [device for device in device_creds_reader]
    print(type(device_creds_list))

print ('\n----- device_creds loaded from CSV as a list fo lists------------------')
pprint( device_creds_list )

#---- Encrypt the device credentials and save into a file
encrypted_dc_out_filename = input('\nGnerate a encrypted file, type a filename: ') or 'encrypted_inventory_creds'
#----encrypt() the cerdential file
with open( encrypted_dc_out_filename, 'wb' ) as dc_out:
    dc_out.write( encrypt( KEY, json.dumps( device_creds_list ) ) )

print ("The file {f} has been encrypted".format(f=encrypted_dc_out_filename))
#----Decrypt the file and get the cerdentials for further processing
print ('\n... getting credentials from the encrypted file...\n')
with open( encrypted_dc_out_filename, 'rb') as device_creds_file:
    device_creds_json = decrypt( KEY, device_creds_file.read() )
#----Print the a list of lists from decripted file
device_creds_list = json.loads( device_creds_json.decode('utf-8'))
pprint( device_creds_list )

print ('\n----- confirm: device_creds in json format------------------------------')

# converting to dictionary of lists using dictionary comprehension
device_creds = { dev[0]:dev for dev in device_creds_list }
pprint( device_creds )
