#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.op.routes import RouteTable
from jnpr.junos.op.routes import RouteSummaryTable

dev = Device(host='192.168.122.10', user='devop', password='junOSxp', gather_facts=False)
dev.open()

tbl = RouteTable(dev)
tbl.get()
#tbl.get("192.168.122.0/24", protocol='bgp')
print (tbl)
for item in tbl:
    print ("#" * 60)
    print ('protocol:', item.protocol)
    print ('age:', item.age)
    print ('via:', item.via)
#    print ('Active:', item.active)
#    print ('Total:', item.total)
#    print ('Routes:', item.route-table)

dev.close()
