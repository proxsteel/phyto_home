#!/usr/bin/env python3
import re   #reular expression
import sys
import yaml
#step1.1
def get_yaml(file_name=None):
    """Basic function that returns a data structure from yaml file.
    Parameters: File name of YAML file.
    """
    if file_name is None:
        raise ValueError("No YAML file passed to function!")
    try:
        return yaml.load_all(open(file_name))
    except IOError:
        print('Ooops! Check the name of the YAML file passed as an argument.')
        print('The file passed during execution does not appear to exist.')
#step1.2
def mormalize_macs(network_data):
    """Iterates over network_data and return a dictionary mapping hostname to MAC address.
    Parameters: Network Data as a dictionary
    """
    host_macs = {}
    #step1.3
    mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[\.:-]?){5}([0-9A-Fa-f]{2})$')
    for document in network_data:
        #print(document, type(document))
        #for hostname, device_data in document.iteritems():
        """iteritems() - only python2  """
        for hostname, device_data in document.items(): #for python3
            #print (hostname, device_data)
            #stiil step1.3
            if mac_regex.match(device_data['mac_address']):
                #print(hostname, device_data['mac_address'])
                #step1.4 return a Dictionary
                host_macs[hostname] = "".join(re.findall(r'[0-9A-Fa-f]+',
                                           device_data['mac_address'].upper()))
            else:
                host_macs[hostname] = None
    #step1.4
    return(host_macs)

def main():
    """Iterates over data structure imported from YAML file
    Parameters: None
    """
    if len(sys.argv) != 2:  #sys.argv[0] == script-name; sys.argv[1..n] == passed arguments#
        print('Ooops! Might want to check your syntax!')
        print('Here is an example how to use:')
        print('python2/3 {xf} <NAME OF YAML FILE>'.format(xf=__file__))
        #__file__ variable returns the file is loaded and run in this case is the script name. 
        sys.exit()
    else:
        _YAML_FILE_ = sys.argv[1]
        network_data = get_yaml(_YAML_FILE_)
        #print(network_data, type(network_data))
        host_macs = mormalize_macs(network_data)
        #step1.4
        print(host_macs)

if __name__ == '__main__':
    main()
