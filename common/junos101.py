"""
junos101.py
   Just a place to put functions that a bunch of scripts
   are going to use.
"""

from jnpr.junos import Device
from ipaddress import *
from getpass import *


def getIPcreds():
    """
    Prompts the user for a hostname, username, and password
    Returns the values in a list
    """
    host_ip = ""
    username = ""
    userpass = ""

    while (host_ip == ""):
        try:
            host_ip = ip_address(input("\nEnter IP address of device to check: "))
        except ValueError:
            print("That does not appear to be a valid IPv4 or IPv6 address.\n")

    while (username == ""):
        username = input("Username: ")

    while (userpass == ""):
        userpass = getpass()

    return ([str(host_ip), username, userpass])


# Opening connections
def jopen(hosts, username, userpass):
    openHosts = {}

    for name, ip in hosts.items():
        devName = Device(host=ip, user=username, password=userpass)

        try:
            devName.open()
            openHosts.update({name: devName})

        except ConnectionError as err:
            print(err)
            print(err._orig)

    return openHosts


# Closing connections
def jclose(hostsOpened):
    for host in hostsOpened:
        host.close()

    return

