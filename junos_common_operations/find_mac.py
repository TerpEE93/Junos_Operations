"""
find_mac.py
    Python script that searches a  host for a given MAC address and
    returns hits where the associated interface name is not a VTEP.
"""

# Imports
from jnpr.junos import Device
from .common.automation_helpers import *
from .op.l2ng_ethernetswitchingtable import *


# Fun with functions
def findMAC(d, mac_addr):
    """
    Given a Device object (d) and a MAC address string (mac_addr),
    execute the Junos RPC for "show ethernet switching table" and
    check the results for the given MAC address.  If it exists in
    the table, report only interfaces that are not VTEP interfaces.
    """
    mac_found = False

    print("\nSearching for MAC address {} on {}...".format(mac_addr, str(d)))
    print("This device appears to be a {}.".format(str(d.facts['model'] )))

    #with d as dev:
    eth_table = L2NG_EthernetSwitchingTable(d)
    eth_table.get(address = mac_addr)

    for mac in eth_table:
        if (mac.mac_address == mac_addr):
            mac_found = True

            if (mac.interface.startswith("vtep")):
                print("\nFound MAC address {} on a VTEP, not locally.".format(mac_addr))
                print("Active source is reported as {}.\n".format(mac.active_source))
            else:
                print("\nMAC address {} is on port {}.\n".format(mac_addr, mac.interface))

    if (not mac_found):
        print("\nMAC address {} not found in this fabric.\n".format(mac_addr)) 

    return


# If we're called directly
if (__name__ == "__main__"):
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-d", "--device", dest = "device", type = str,
                        help = "IP address of target device")
    parser.add_argument("-m", "--mac_addr", type = str, dest = "mac",
                        help = "MAC address to find")
    parser.add_argument("-u", "--user", type = str, dest = "user", help = "Username")
    parser.add_argument("-p", "--password", type = str, dest = "password", help = "Password")

    args = parser.parse_args()

    dev_ip = validateIP(args.device)
    mac_addr = validateMAC(args.mac)
    user = validateUser(args.user)
    password = validatePassword(args.password)

    d = Device(host = dev_ip, user = user, password = password)

    try:
        d.open()
    except ConnectionError as err:
        print("\nCan't connect to device: {0}".format(err))
    except Exception as err:
        print("\nError: {0}".format(err))

    if (d.connected):
        findMAC(d, mac_addr)
        d.close()

# C'est tout, mes amis...