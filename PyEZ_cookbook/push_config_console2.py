#!/usr/bin/env python3
#Written for JunOS Atomation time
#NETCONF is disabled by default
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConfigLoadError
from lxml import etree
#from pathlib import Path #windows needs it ...
import getpass
import time
import sys
import os
import logging
#https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
#########################################################################
#This scripts woks only on linux systems, not working on Windows, yet.
#########################################################################
SERIAL_PORT = "/dev/ttyUSB0"
UNAME = input("Username: ") #with passfrase
#if UNAME != "root":
PW = getpass.getpass("Password: ")   #if the username is root hit enter, by default no password
#else:
#    PW = "\n"
#########################################################################
CONFIG_FILE = input("Config-file-name: ")
#DATA_FOLDER = Path("SEA3-Refresh/")
#DATA_FOLDER = os.getcwd()

#enable the below line for debugging PyEZ/NETCONF
logging.basicConfig(level=logging.ERROR)

def main():
    try:
        with Device(user=UNAME, passwd=PW, mode='serial',port="/dev/ttyUSB0", gather_facts=False, timeout=10) as EXdev:
            print ("...Checking connection ...\n...............................\n...Connection established: {checkit}".format(checkit=EXdev.connected))
            print(EXdev.cli("show version", format='text', warning=False))
            cfg = Config(EXdev)
            start_time = time.time()
            cfg.lock()
            #cfg.load('delete', format='set')
            #cfg.load('set system host-name TEMP', format='set')
            #cfg.load('set system root-authentication encrypted-password "$1$MuK2KPdi$YZbi17SXuxiN7D3gCzkPq/"', format='set')
            #cfg.load('set system services netconf traceoptions file xyz', format='set')
            #cfg.commit(comment="****** Errazing the factory config done******", timeout=10)
            #cfg.pdiff()
            #cfg.lock()
            cfg.load(path=CONFIG_FILE, merge=True)
            cfg.pdiff()
            cfg.commit_check()
            print("Pushing the commit command...") 
            cfg.commit(timeout=15)
            cfg.unlock()
            print("Commit completed...")
            #print(EXdev.cli("show configuration | no-more", format='text', warning=False))
            print("Closing connection to device ...\nThe loading has been completed in {sec} seconds".format(sec=time.time() - start_time))
            #dev.close()
    except ConnectError as err:
        print ("{t} Cannot connect to device: {e}".format(t=time.asctime(), e=err))
        sys.exit(1)
    except ConfigLoadError as err:
        print ("{t} Unable to load the configuration due to: {e}".format(t=time.asctime(), e=err))
        sys.exit(1)
    except Exception as err:
        print ("{t} --+== {e} ==+--".format(t=time.asctime(), e=err))
        sys.exit(1)

if __name__ == '__main__':
    main()
