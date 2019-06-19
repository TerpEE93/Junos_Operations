"""
devices.py
   Class definitions for a bunch of Junos devices
"""

class Switch(object):
    def __init__(self):
        self.host_port_prefix = ""
        self.uplink_port_prefix = ""
        self.host_port_count = 0
        self.uplink_port_count = 0
        self.host_ports = []
        self.uplink_ports = []
        self.vc_ports = []
        self.mgt_port = "em0"

    def buildHostPortsList(self, host_port_prefix, host_port_count):
        ports_list = []
        for i in range(0, host_port_count):
            portname = self.host_port_prefix + "-0/0/" + str(i)
            self.host_ports.append(portname)

    def buildUplinkPortsList(self, uplink_port_prefix, host_port_count, uplink_port_count):
        ports_list = []
        for i in range(host_port_count, (host_port_count + uplink_port_count)):
            portname = self.uplink_port_prefix + "-0/0/" + str(i)
            self.uplink_ports.append(portname)

class QFX5100_48S(Switch):
    def __init__(self):
        self.host_port_prefix = "xe"
        self.uplink_port_prefix = "et"
        self.host_port_count = 48
        self.uplink_port_count = 6
        self.mgt_port = "em0"

        self.host_ports = []
        self.uplink_ports = []

        self.buildHostPortsList(self.host_port_prefix, self.host_port_count)
        self.buildUplinkPortsList(self.uplink_port_prefix, self.host_port_count, self.uplink_port_count)

        self.vc_ports = self.uplink_ports[len(self.uplink_ports)//2:]

class QFX5120_48Y(Switch):
    def __init__(self):
        self.host_port_prefix = "et"
        self.uplink_port_prefix = "et"
        self.host_port_count = 48
        self.uplink_port_count = 8

        self.host_ports = []
        self.uplink_ports = []

        self.buildHostPortsList(self.host_port_prefix, self.host_port_count)
        self.buildUplinkPortsList(self.uplink_port_prefix, self.host_port_count, self.uplink_port_count)

        self.vc_ports = self.uplink_ports[len(self.uplink_ports)//2:]



# END