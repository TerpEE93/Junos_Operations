"""
check_bgp.py
    Python script that checks the health of BGP sessions on one or more
    device running Junos.  First check runs "show bgp summary" and reports
    up/down status on configured peers.  Maybe there will be more later.
"""

# Imports
from jnpr.junos import Device
from common.automation_helpers import *
from common.junos101 import checkLocalIFL
from op.bgpHealth import *


# The fun stuff
def checkBGP(d):
    """
    Given a device object (d), check execute the RPC for "show bgp neighbors"
    are print out details about the state of each peering session.  Print a
    list of sessions not in the Established state at the end so the user can
    quickly identify the problem children.
    """
    down_peers = []

    print("\nChecking BGP health on {}...".format(str(d)))

    bgp_table = BGPNeighborTable(d)
    bgp_table.get()

    for peer in bgp_table:
        peer_ip = peer.peer_address.split("+")[0]
        local_ip = peer.local_address.split("+")[0]
        
        print("\nPeer {} is in state {}.".format(peer_ip, peer.state))
        print("    Peering interface: {}    Local address: {}".format(peer.local_ifl, local_ip))
        print("    Local AS: {}    Peer AS: {}".format(peer.local_as, peer.peer_as))
        print("    Peering type: {}    Peer group: {}".format(peer.type, peer.peer_group))
        print("    Address families: {}".format(peer.nlri))
        print("    Last reported error: {}".format(peer.last_error))

        if (peer.state != "Established"):
            down_peers.append([peer_ip, local_ip])

    if (len(down_peers) != 0):
        print("\n\nThe following peers appear to be down:")
          
        for peer in down_peers:
            print("  - {}".format(peer[0]))
            local_if = checkLocalIFL(d, peer[1])

            if (local_if):
                print("      Local address {} is on interface {}, state is {}".format(peer[1], local_if[0], local_if[1]))
                
                if (local_if[1] == "up"):
                    result = d.rpc.ping(host=peer[0], source=peer[1], count="3", interval="1", wait="1")

                    if ( result.findtext('.//packet-loss') == '\n0\n' ):
                        print("      {} is reachable from {}.".format(peer[0], peer[1]))
                    elif ( result.findtext('.//packet-loss') == '\n100\n' ):
                        print("      {} is NOT reachable from {}.".format(peer[0], peer[1]))
                    else:
                        print("      {} is INTERMITTENTLY reachable from {}.".format(peer[0], peer[1]))

            else:
                print("      Local address {} does not exist on this device.".format(peer[1]))


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

    d = Device(host = dev_ip, user = user, password = password)

    try:
        d.open()
    except ConnectionError as err:
        print("\nCan't connect to device: {0}".format(err))
    except Exception as err:
        print("\nError: {0}".format(err))
    
    if (d.connected):
        checkBGP(d)
        d.close()


# END