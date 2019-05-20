#!/usr/bin/env python3

from ncclient import manager
import sys


# the variables below assume the user is leveraging the
# student lab and accessing srx_r1 using the loopback
HOST = '192.167.122.10'
# use the NETCONF port for your srx_r1 device
PORT = 830
# use the user credentials for your srx_r1 device
USER = 'devop'
PASS = 'junOSxp'


# Basic main() method
def main():
    """
    Main method that prints netconf capabilities of remote device.
    """
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         look_for_keys=False, allow_agent=False) as m:

        # print all NETCONF capabilities
        print('* Here are the Remote Devices Capabilities *')
        for capability in m.server_capabilities:
            print(capability.split('?')[0])

if __name__ == '__main__':
    sys.exit(main())
