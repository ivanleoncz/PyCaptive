
import socket
import subprocess as sp
import sys
from app import TEST, IPTABLES, CONNTRACK, DB_ADDR, DB_PORT
from app import GLOBAL_CONF as v


class Components():


    def __init__(self):
        self._binaries = (IPTABLES, CONNTRACK)
        self._services = None

        if TEST:
            self._services = {"mongodb": (DB_ADDR, DB_PORT)}
        else:
            self._services = {
                             "nginx": (v["LAN_IP"], v["NGINX_REDIR_GUNICORN"]),
                             "mongodb": (DB_ADDR, DB_PORT)
            }


    def binaries(self):
        """ Check existence of binaries. """
        results = dict()
        for b in self._binaries:
            result = sp.call(["which", b], stderr=sp.DEVNULL, stdout=sp.DEVNULL)
            result_bin = b.split('/')[-1]
            if result == 0:
                results[result_bin] = 0
            else:
                results[result_bin] = 1
        return results


    def services(self):
        """ Check status of network services. """
        # TODO: must ensure that this is working....
        results = dict()
        for k,v in self._services.items():
            s = socket.socket()
            try:
                s.connect((v[0], int(v[1])))
                results[k] = 0
            except Exception:
                results[k] = 1
            finally:
                s.close()
        return results
