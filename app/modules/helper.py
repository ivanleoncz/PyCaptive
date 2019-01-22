""" Provides helper functions. """

import subprocess as sp
import sys


def get_nic_ip(nic):
    """ Get IP address from a NIC."""
    result = sp.check_output(["ip", "addr", "show", nic])
    result = result.decode().split()
    try:
        ipaddr = result[result.index('inet') + 1].split('/')[0]
        return ipaddr
    except Exception:
        print("Helper ERROR: no network configuration was detected for LAN_NIC")
        sys.exit(1)
