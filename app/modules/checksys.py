
import socket
import subprocess as sp
import sys
from app import TEST_MODE
from app import checksys_dict as d


class Components():


    def __init__(self):
        self._binaries = (d.get("IPTABLES"), d.get("CONNTRACK"))
        self._services = None

        if TEST_MODE:
            self._services = {
                               "mongodb":(
                                 d.get("MONGODB_IP"), d.get("MONGODB_PORT")
                               )
                             }
        else:
            self._services = {
                               "nginx_redir_gunicorn":(
                                 d.get("NGINX_IP"), d.get("NGINX_REDIR")
                               ),
                               "nginx_gunicorn":(
                                 d.get("NGINX_IP"), d.get("NGINX_GUNICORN")
                               ),
                               "mongodb":(
                                 d.get("MONDODB_IP"), d.get("MONGODB_PORT")
                               )
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
