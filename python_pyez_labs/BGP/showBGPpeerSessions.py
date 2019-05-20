#!/usr/bin/env python3
"""
PyEZ Custom BGP Tables and Views
"""
from jnpr.junos import Device
from jnpr.junos.exception import *
from bgp import BGPNeighborTable
import sys, time

# step 1.1
def main():
    """Simple main method to enter log entries."""
    ROUTERS = ['192.168.122.10', '192.168.122.20']
    op_user = 'devop'
    op_pass = 'junOSxp'
    for router in ROUTERS:
        try:
            dev = Device(host=router, user=op_user, passwd=op_pass)
            dev.open()
            dev_info = BGPNeighborTable(dev)
            dev_info.get()
            for key in dev_info.keys():
                bgp_info = dev_info[key]
                print('#' * 60)
                print('This host         : {host}'.format(host=bgp_info.local_address))
                print('Belongs to ASN    : {ver}'.format(ver=bgp_info.local_as))
                print('And peers with    : {host}'.format(host=bgp_info.peer_address))
                print('In ASN            : {ver}'.format(ver=bgp_info.peer_as))
                print('The peer type is  : {ver}'.format(ver=bgp_info.peer_type))
                print('The peer state is : {flap}'.format(flap=bgp_info.peer_state))
                print('The peer is advertising   : {sent}'.format(sent=bgp_info.nlri_type_peer))
                print('We peer are advertising   : {recv}'.format(recv=bgp_info.nlri_type_session))
                print('We are applying policy    : {act}'.format(act=bgp_info.export_policy))
                print('With route preference     : {recv}'.format(recv=bgp_info.preference))
                print('Using holdtime            : {acc}'.format(acc=bgp_info.holdtime))
                print('#' * 60)
        except ConnectError as err:
            print ("{t} Connection Error: {e}".format(t=time.asctime(), e=err))
            pass
        except Exception as err:
            print ("Exception Error: {e}".format(e=err))
            sys.exit(1)
        finally:
            dev.close()

if __name__ == '__main__':
    main()
 
