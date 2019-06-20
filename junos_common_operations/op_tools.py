"""
This is a front-end for calling operational tools.
"""

from sys import exit
from jnpr.junos import Device
from .common.automation_helpers import *

from .find_mac import findMAC
from .check_bgp import checkBGP
from .check_vc_links import checkVCLinks

from argparse import ArgumentParser



def drawMenu(context, menu_dict, dev_ip, username, password):
    """
    Takes a dictionary where the key is the option string the user presses
    and the value is the text string that describes the option.

    This just draws the menu.  It returns nothing.
    """
    print("\n")
    
    if (context == "admin"):
        print("Admin Menu")
        print("==========")

    elif (context == "operations"):
        print("Operations Menu")
        print("===============")

    for key, value in menu_dict.items():
        print("{}:  {}".format(key, value))

    print("\n")
    
    print("Device is: {}".format(dev_ip))
    print("Username is: {}".format(username))

    if (password == ""):
        print("Password is NOT set.")
    else:
        print("Password is set.")

    print("\n")

    return


def waitForInput():
    """
    Does what it says, it waits for input from the user.
    That is all...
    """

    input("\nPress [Enter] to return to the menu...")


def main():
    admin_dict = { "1": "Set/change target device",
                   "2": "Set/change username",
                   "3": "Set/change password",
                   "4": "Open connection to device",
                   "Q": "Quit this application"}

    oper_dict = { "1": "Find MAC address on a switch/fabric",
                  "2": "Check BGP health of a network device",
                  "3": "Validate \"VC\" cabling of a two-member EVPN fabric",
                  "C": "Close connection to device and return to Admin Menu"}

    choice = ""
    mac_addr = ""

    target = ""
    username = ""
    password = ""

    context = "admin"

    parser = ArgumentParser()
    parser.add_argument("-d", "--device", dest = "target", type = str,
                        help = "IP address of target device")
    parser.add_argument("-u", "--user", type = str, dest = "username", help = "Username")
    parser.add_argument("-p", "--password", type = str, dest = "password", help = "Password")

    args = parser.parse_args()

    print("\n\nWelcome to the op_tools script - a frontend for executing")
    print("common operational tasks on Junos devices.  Please choose from")
    print("the options listed below.  You will be prompted for additional")
    print("information required to execute the task.\n")

    while True:

        while (context == "admin"):
            drawMenu(context, admin_dict, target, username, password)
            choice = str(input("Please make a selection: "))

            if (choice == "1"):
                target = ""
                target = validateIP(target)

            elif (choice == "2"):
                username = ""
                username = validateUser(username)

            elif (choice =="3"):
                password = ""
                password = validatePassword(password)

            elif (choice == "4"):
                target = validateIP(target)
                username = validateUser(username)
                password = validatePassword(password)

                dev = openDevice(target, username, password)
            
                if (dev):
                    if (dev.connected):
                        context = "operations"
                        print("\nConnected to {}...".format(dev))

            elif (choice == "q" or choice == "Q"):
                exit()

            else:
                pass

        while (context == "operations"):
            drawMenu(context, oper_dict, target, username, password)
            choice = str(input("Please make a selection: "))
        
            if (choice == "c" or choice =="C"):

                if (dev):
                    if (dev.connected):
                        context = "admin"
                        print("\nClosing connection to {}...".format(dev))
                        dev.close()

                break

            elif (choice == "1"):
                mac_addr = ""
                mac_addr = validateMAC(mac_addr)
                findMAC(dev, mac_addr)
                waitForInput()

            elif (choice == "2"):
                checkBGP(dev)
                waitForInput()

            elif (choice == "3"):
                checkVCLinks(dev)
                waitForInput()

            else:
                pass



# If we're called directly
if (__name__ == "__main__"):

    main()        


# END