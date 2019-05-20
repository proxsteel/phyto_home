#!/usr/bin/env python3
from napalm import get_network_driver
import time
import multiprocessing

UN = "devop"
PW = "ciscoxp"
INVENTORY = "config1.txt"
LOG = "log.txt"
optional_arg = {'dest_file_system': 'nvram:'}
with open(INVENTORY) as f:
    DEVICE = f.read().splitlines()

def write(ip, bufe, fo):
    file = open(fo, 'a')
    file.write(ip + ' ')
    file.write(str(bufe))
    file.write('\n')
    file.close()

def host(ip):
    try:
        driver = get_network_driver('ios')
        device = driver(ip, UN, PW, timeout=30, optional_args=optional_arg)
        device.open()
        output = device.get_facts()
#        print (output)
        out = device._send_command('show clock')
        outz = device.cli('show version')
        scp_enable = device.load_merge_candidate(config='password encryption aes ')
        #needs scp to be enabled even its config param instead of filename
        #load_config = device.load_merge_candidate(filename='Prefix_list.cfg')
        merge = device.commit_config()
        print(ip, '--', out)
        write(ip, out, LOG)
        device.close()
    except Exception as e:
        print(ip, str(e))
        write(ip, str(e), LOG)


def main():
    start_time = time.time()
#    print(len(DEVICE))
    with multiprocessing.Pool(processes=10) as process_pool:
        process_pool.map(host, DEVICE)
        process_pool.close()
        process_pool.join()
    print("Finished in %f sec." % (time.time() - start_time))


if __name__ == "__main__":
    main()
