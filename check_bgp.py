"""
check_bgp.py
    Python script that checks the health of BGP sessions on one or more
    device running Junos.  First check runs "show bgp summary" and reports
    up/down status on configured peers.  Maybe there will be more later.
"""

# Imports
from jnpr.junos import Device
from common.automation_helpers import *
from op.bgpHealth import *


# The fun stuff
def checkBGP(d):
    """
    This does something.
    """
    down_peers = []

    print("\nChecking BGP health on {}...".format(str(d)))

    with d as dev:
        bgp_table = BGPNeighborTable(dev)
        bgp_table.get()

    for peer in bgp_table:
        print("\nPeer {} is in state {}.".format(peer.peer_address, peer.state))
        print("    Peering interface: {}    Local address: {}".format(peer.local_ifl, peer.local_address))
        print("    Local AS: {}    Peer AS: {}".format(peer.local_as, peer.peer_as))
        print("    Peering type: {}    Peer group: {}".format(peer.type, peer.peer_group))
        print("    Address families: {}".format(peer.nlri))
        print("    Last reported error: {}".format(peer.last_error))

        if (peer.state != "Established"):
            down_peers.append(peer.peer_address)

    if (len(down_peers) != 0):
        print("\nThe following peers appear to be down:")
          
        for peer in down_peers:
            print("  - {}".format(peer))

        print("\nCheck output above for local config details.")
        print("Also run this check on the remote peer(s) and compare results.")

    print("\n")    
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

    target.open()
    
    checkBGP(target)
    target.close()


# END