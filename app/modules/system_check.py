

import socket
import subprocess as sp
import sys


binaries = [IPTABLES, CONNTRACK]
services = None

if TEST:
    services = { "mongodb": (DB_ADDR, DB_PORT) }
else:
    try:
        result = sp.check_output(["ip", "addr", "show", LAN])
        result = result.split()
        ipaddr = result[result.index('inet') + 1].split('/')[0]
        services = {
                        "nginx": (ipaddr, 14901),
                        "mongodb": (DB_ADDR, DB_PORT)
                    }
    except Exception:
        print("ERROR: check pycaptive_settings.py (IPTABLES section)")
        sys.exit(1)


def check_binaries(binaries):
    """ Check existence of binaries. """
    for b in binaries:
        result = sp.call(["which", b], stderr=sp.DEVNULL, stdout=sp.DEVNULL)
        result_bin = b.split('/')[-1]
        if result == 0:
            print("{0:10} {1:12}: {2}".format("binary", result_bin, "OK"))
        else:
            print("{0:10} {1:12}: {2}".format("binary", result_bin, "NOK"))


def check_service(services):
    """ Check status of a network service. """
    for k,v in services.items():
        s = socket.socket()
        try:
            s.connect((v[0], int(v[1])))
            print("{0:10} {1:12}: {2}".format("service", k, "OK"))
        except Exception:
            print("{0:10} {1:12}: {2}".format("service", k, "NOK"))
        finally:
            s.close()


check_binaries(binaries)
check_service(services)
