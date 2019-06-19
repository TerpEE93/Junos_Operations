"""
junos101.py
   Just a place to put functions that a bunch of scripts
   are going to use.
"""

from jnpr.junos import Device
from ..op.interfaceTables import *

def checkLocalIFL(d, ipa):
    """
    Given a device object (d) and valid IP address (ipa), find and return
    the interface on the device that holds that address and it's state.  If there is no
    interface on the device with that IP address, return a value of None.
    """
    target_ifl = None
    target_state = None

    ifTable = intTerseTable(d)
    ifTable.get()

    for ifl in ifTable:
        if (ifl.address):
            address = str(ifl.address).split("/")[0]

            if (address == ipa):
                target_ifl = ifl.ifl
                target_state = ifl.state

    return [target_ifl, target_state]
