""" Provides helper functions. """

def get_nic_ip(nic):
    """ Get IP address from a NIC."""
    import subprocess as sp
    result = sp.check_output(["ip", "addr", "show", nic])
    result = result.decode().split()
    ipaddr = result[result.index('inet') + 1].split('/')[0]
    return ipaddr
