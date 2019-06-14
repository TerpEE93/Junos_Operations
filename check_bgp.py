"""
check_bgp.py
    Python script that checks the health of BGP sessions on one or more
    device running Junos.  First check runs "show bgp summary" and reports
    up/down status on configured peers.  Maybe there will be more later.
"""

# Imports
from jnpr.junos import Device
from common.junos101 import *
from op.bgpHealth import *

# Drop the variables in here
hosts = { 'spine_10': '192.168.250.10', 'spine_11': '192.168.250.11' }
openHosts = {}

username = 'admin'
userpass = 'Juniper1'

# The fun stuff
print("Let's check BGP on hosts:")
for host in hosts:
  print(host)

print("\n\nOpening hosts...")
openHosts = jopen(hosts, username, userpass)


print("\nOpened hosts:")
for host in openHosts:
    print(host)
print("\n")
print(list(openHosts.values()))
print ("\n\n")

"""
The BGP stuff goes here
"""

print("Closing all open connections...")
jclose(list(openHosts.values()))
print("Bye!\n\n")

