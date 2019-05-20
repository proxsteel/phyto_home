Problem:
In order for Juniper PyEZ to connect to your devices, 
you need to confgure the NETCONF daemon in Junos to listen for external connections.

Enabling this functionality is simply a matter of applying the following confguration 
to your device(s): set system services netconf ssh

If your network has a signifcant number of devices, however, logging into every
box to enable NETCONF (and thus Junos PyEZ automation) sounds like a job for
a lucky, enthusiastic, junior network engineer.

Surely we can automate this?!
This recipe explores the use of the netmiko library in Python to execute commands
in Junos directly on the CLI and prepare our network for automation with Junos
PyEZ.

Where PyEZ interacts with Junos via NETCONF,netmiko operates by interacting with 
the Junos CLI (over SSH in this case) sending commands and waiting for a response.
This makes it an extremely useful tool for interacting with devices from vendors
that don’t provide NETCONF or other API mechanisms for programmatic access
