
#!/usr/bin/env python3
#Written for JunOS Atomation time
#NETCONF is disabled by default
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from lxml import etree
from pathlib import Path
import getpass
import time
import sys
import os
import logging
#https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
#########################################################################
#https://www.ftdichip.com/Support/Documents/AppNotes/AN_220_FTDI_Drivers_Installation_Guide_for_Linux.pdf
#########################################################################

#HOST = input("IP address: ")
#print("\nExamples: COM3 for Win or /dev/ttyUSB0 for linux machine\n")
#SERIAL_PORT = "COM3"
#UNAME = input("Username: ") #with passfrase
print("\nTrying to connect...")
#PW = getpass.getpass("Password: ")   #if the username is root hit enter, by default no password 
#PW = "junOS13"
#CONFIG_FILE = input("Config-file-name: ")
#DATA_FOLDER = Path("SEA3-Refresh/")
#DATA_FOLDER = os.getcwd()
logging.basicConfig(level=logging.DEBUG)


def main():
    try:
        with Device(user="dotel", passwd="junOS1314", mode='serial',port="COM3", gather_facts=True, timeout=10) as EXdev:
            print (EXdev.connected)
            #start_time = time.time()
            print(EXdev.facts)
            print(EXdev.cli("show version", format='text', warning=False))
            #cfg = Config(EXdev)
            #cfg.lock()
            #cfg.load(path=DATA_FOLDER+CONFIG_FILE, format='set', overwrite=True) 
            #cfg.commit_check()
            print("Commiting configuration...") 
            #cfg.commit()
            #cfg.unlock()
            print("Closing connection to device ...\nThe load has been completed in {sec} seconds".format(sec=time.time() - start_time))
            #dev.close()
    except ConnectError as err:
        print ("{t} Cannot connect to device: {0}".format(t=time.asctime(), e=err))
        sys.exit(1)
    except Exception as err:
        print ("{t} --+== {e} ==+--".format(t=time.asctime(), e=err))
        sys.exit(1)

if __name__ == '__main__':
    main()
