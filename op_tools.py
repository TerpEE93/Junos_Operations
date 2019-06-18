"""
This is a front-end for calling operational tools.
"""




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