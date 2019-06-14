Just a place to put some modestly-helpful operational scripts that leverage
the Junos PyEZ framework.  Use them if you like, or don't, it's cool.

The usual warnings and disclaimers apply:

1.  I'm not a software engineer.  I'd barely even call myself a programmer.
    These are just simple tools I've put together to make life easier for
    me while testing.  If they also make life easier for you, then bonus!
    But do not expect complete, robust, or by any means pretty code.  Did I
    mention I'd barely call myself a programmer?

2.  Don't expect lots of WOW-factor.  See #1.

3.  I may abandon this at any time and move on to the next shiny object.
    If you don't belive me, check out my other repos.  My attention span is
    limited.


Current scripts:

check_lldp.py
-------------
Purpose-built for lovers of Juniper's Virtual Chassis technology.

So you want to move away from VC in favor of an EVPN-based solution?
This tool will check the cabling between two like-model QFX switches
and report cabling issues between the "VC" ports.  For the purpose
of this exercise, I have declared the upper half of the uplink ports
on a QFX51xx TOR to be the "VC" ports, so for example, et-0/0/51 - 53
on the QFX5100-48S.  So if you want to build an EVPN replacement for
a two-member VC of QFX5100-48S, you would cable one or more of
et-0/0/51 through et-0/0/53 between them.  This script will ensure
that you cabled them correctly.


find_mac.py
-----------
This script will locate the source of a MAC address on a switch.  If the
MAC address shows up on a local port, the script reports the host port
associated with the MAC address.  If the MAC address shows up on a VTEP
interface, then the script just reports that.