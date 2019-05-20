#!/usr/bin/env python3
from jnpr.junos import Device
from jnpr.junos.exception import *
from pprint import pprint
import sys, re, os, time
import sqlite3

# step 1.2 writing logs to sqlite DB
def write_logs_to_db(db, log):
    """write log entry to database"""
    try:
        db_connection = sqlite3.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS logs (timestamp VARCHAR(20) PRIMARY KEY,
                                                              hostname VARCHAR(8),
                                                              interface VARCHAR(20),
                                                              message VARCHAR (30))''')
        sql_cmd = 'INSERT INTO logs (timestamp, hostname, interface, message) VALUES (?,?,?,?)'
        db_cursor.execute(sql_cmd, (log[0], log[1], log[2], log[3]))
        db_connection.commit()
    except sqlite3.IntegrityError as E:
        print("Avoiding duplicate entries.")
        print("Here is the error {error}".format(error=E))
    finally:
        db_connection.close()

# step 1.1
def main():
    """Simple main method to enter log entries."""
    ROUTERS = ['192.168.122.10', '192.168.122.20']
    op_user = 'devop'
    op_pass = 'junOSxp'
    netdata_db = 'network_data.db'
#step 1.3 coment all print statements and use compile() method to create a regex to extract the link down messages
#step 1.3 finditer() method to retrive all matching log messages
#original REGEX: ('(\w{1,3}\s{1,3}\d{1,2}\s{1,3}\d{1,2}:\d{1,2}:\d{1,2}).*SNMP_TRAP_LINK_DOWN.*ifName ([gax]e-\d{1,2}\/\d{1,2})\n')
#https://www.regextester.com/
    link_down = re.compile('(\w{1,3}\s{1,3}\d{1,2}\s{1,3}\d{1,2}:\d{1,2}:\d{1,2}).*SNMP_TRAP_LINK_DOWN.*ifName (em[0-9])')
    for router in ROUTERS:
        try:
            device = Device(host=router, user=op_user, passwd=op_pass)
            print ('Connecting to device {r}'.format(r=router))
            device.open()
            #pprint (device.facts)
# step 1.2 coment pprint statment
            logs = device.rpc.get_log(filename='messages')
            for log_content in logs.iter("file-content"):
                #print (type(log_content))
                #print (dir(log_content))
                #print (log_content.text)
                messages = link_down.finditer(log_content.text)
                # step1.3
                if messages:
                    for log in messages:
                        entry = []
                        #step 1.3
                        #print(log.group(0))
                        #print(log)
                        #step 1.4
                        #group() method: 1 is the first () in compile() and 2 is the second
                        #group 0 is the entire message that match
                        print("Starting DownTime: ", log.group(1))
                        print("Interface Name: ", log.group(2))
                        print("Whole message: ", log.group(0))
                        #print(log.group(1).replace(' ', '_') + '_' + device.facts['fqdn'])
                        entry.append(log.group(1).replace(' ', '_') + '_' + device.facts['fqdn'])
                        entry.append(device.facts['fqdn'])
                        entry.append(log.group(2))
                        entry.append(log.group(0))
                        write_logs_to_db(netdata_db, entry)
           # device.close()
        except Exception as e:
            print ("We have a problem retrieving the information")
            print ('Here is the error {error}'.format(error=e))
        finally:
           device.close()
if __name__ == "__main__":
    sys.exit(main())
