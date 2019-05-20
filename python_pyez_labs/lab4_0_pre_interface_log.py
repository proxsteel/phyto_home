#!/usr/bin/env python
from jnpr.junos import Device
from jnpr.junos.exception import *
from jnpr.junos.utils.config import Config
from jnpr.junos.cfg.phyport import PhyPortClassic
import sys
import time

def main():
    """Simple main method to enter log entries."""
    ROUTERS = ['192.168.122.10', '192.168.122.20']
    op_user = 'devop'
    op_pass = 'junOSxp'
    sessions = [Device(host=ROUTER, user=op_user, passwd=op_pass) for ROUTER in ROUTERS]
    for session in sessions:
        session.open()
        port = PhyPortClassic(session, namevar='em3')
#step 1.1
       # print(port.properties)
       # print(port.admin)
       # step 1.2
        port.admin = False
        port.write() #write changes to the canditate config
        print("Desabling the Interface!")
        cfg = Config(session)
        cfg.commit()
        time.sleep(10)

        port.admin = True
        port.write()

        print("Enabling the Interface")
        cfg.commit()
        session.close()

if __name__ == '__main__':
    sys.exit(main())
