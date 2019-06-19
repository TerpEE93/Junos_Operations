"""
check_vc_links.py
    Python script that checks the status of LLDP to determine
    whether or not the inter-switch cabling for a VC replacement
    is correct.

    This script assumes that: (a) the VC replacement consists of
    exactly two like-model switches, and (b) that the the upper-half
    of the uplink ports are reserved for VC inter-connect."
"""

# Imports
from jnpr.junos import Device
from common.automation_helpers import *
from common.devices import *
from op.lldpNeighbor import *


def checkVCLinks(d):
    """
    Given a device object (d), execute the Junos RPC for
    "show lldp neighbor interfaces" and check the results for the "VC"
    ports.  We expect that a VC port on the local switch will be connected
    to a like-named VC port on the peer switch.  We will report the errors.
    """
    dev_model = str(d.facts['model'])
    print("\nThis device appears to be a {}.".format(dev_model))

    switch_type = matchDevice(dev_model)
    if (len(switch_type.vc_ports) != 0):
        print("Checking LLDP neighbors on {}.".format(str(d)))

        lldp = LLDPNeighborTable(d)
        lldp.get()

        for port in lldp:
            if (port in switch_type.vc_ports):
                print("{} has neighbor {} on node {}".format(port.local_if, port.remote_if, port.remote_dev))

                if (port.local_if != port.remote_if):
                    print("\n*** Cabling Error ***")
                    print("{} should connect to {} on node {}\n".format(port.local_if, port.local_if, port.remote_dev))
    
    else:
        print("Can't check LLDP on unidentified switch type.\n")

    return


# If we're called directly
if (__name__ == "__main__"):
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-d", "--device", dest = "device", type = str,
                        help = "IP address of target device")
    parser.add_argument("-u", "--user", type = str, dest = "user", help = "Username")
    parser.add_argument("-p", "--password", type = str, dest = "password", help = "Password")

    args = parser.parse_args()

    dev_ip = validateIP(args.device)
    user = validateUser(args.user)
    password = validatePassword(args.password)

    target = Device(host = dev_ip, user = user, password = password)

    try:
        d.open()
    except ConnectionError as err:
        print("\nCan't connect to device: {0}".format(err))
    except Exception as err:
        print("\nError: {0}".format(err))

    if (d.connected):
        checkVCLinks(target)
        target.close()


# END