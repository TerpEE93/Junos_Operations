"""
automation_helpers.py
   Just a place to put functions that a bunch of scripts
   are going to use.
"""

from netaddr import *
from getpass import getpass
from ipaddress import ip_address
from jnpr.junos import Device
from common.devices import *


def validateIP(ipa):
    """
    Uses ipaddress.ip_address() to ensure that we have a valid and
    properly-formatted IP address.

    Expects a string.
    Returns an ip_address object.
    """
    good_ip = ""

    while (good_ip == ""):
        try:
            good_ip = ip_address(ipa)
        except ValueError:
            ipa = input("\nPlease enter a valid IPv4 or IPv6 address for the target device: ")

    return str(good_ip)


def validateMAC(mac):
    """
    Uses netaddr.EUI() to ensure that we have a valid and
    properly-formatted MAC address.

    Expects a string.
    Returns a string - MAC address in "mac_unix_expanded" format.
    """
    good_mac = ""

    while (good_mac == ""):
        try:
            good_mac = EUI(str(mac))
        except AddrFormatError:
            mac = input("\nPlease enter a valid MAC address to search for: ")

    good_mac.dialect = mac_unix_expanded

    return str(good_mac)


def validateUser(user):
    """
    Just checks to make sure we have something that looks like a username.

    Expects a string.
    Returns a string.
    """
    while (user == ""):
        user = input("Username: ")

    return user

def validatePassword(password):
    """
    Just checks to make sure we have something that looks like a password.

    Expects a string.
    Returns a string.
    """
    while (password == ""):
        #password = input("Password: ")
        password = getpass("Password: ")

    return password

def matchDevice(model):
    """
    Given a string of the device model returned by Device.facts, check it
    against our list of device classes and return an object of the proper
    device class.

    Add more devices as necessary.
    """
    if (model.startswith("QFX5100-48S") or model.startswith("QFX5100E-48S")):
        dev_type = QFX5100_48S()
    elif (model.startswith("QFX5120-48")):
        dev_type = QFX5120_48Y()
    else:
        print("\nError: Unable to match device to a model.\n")
        dev_type = Switch()

    return dev_type


def openDevice(ip_address, user, password):
    """
    Takes an IP address, username, and password, and attempts to open a
    connection to the target device.  Returns a Device object if successful.
    """
    ipa = validateIP(ip_address)
    usr = validateUser(user)
    pwd = validatePassword(password)

    d = Device(host = ipa, user = usr, password = pwd)

    try:
        d.open()
    except ConnectionError as err:
        print("\nCan't connect to device: {0}".format(err))
        return None
    except Exception as err:
        print("\nError: {0}".format(err))
        return None

    return d


# END