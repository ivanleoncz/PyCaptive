#!/usr/bin/python3
""" Allowing/prohibiting INTERNET access based on IP addresses.

This module is responsible for allowing/prohibiting INTERNET access by means
of IPTABLES/Netfilter rules for IP addresses from the devices were PyCaptive
users have successfully authenticated.

NOTICE: adjust class variables, according to your setup.
"""

from datetime import datetime
from app import log

__author__ = "@ivanleoncz"

import subprocess as sp


class Worker:
    """ IPTABLES/Netfilter rules for allowing/prohibiting INTERNET access. """

    binnary = "/sbin/iptables"
    table   = "mangle"
    chain   = "PREROUTING"
    nic     = "eth2"
    jump    = "INTERNET"

    def add_rule(self, ip):
        """ Allowing INTERNET access. """
        rule = [self.binnary, "-t",self.table, "-I", self.chain,
                     "-i", self.nic, "-s", ip, "-j", self.jump]
        try:
            result = sp.call(rule)
            ts = datetime.now()
            if result == 0:
                log.error('[%s] %s %s %s %s',
                  ts, "iptables", "add_rule", ip, "OK")
                return 0
            else:
                log.error('[%s] %s %s %s %s',
                  ts, "iptables", "add_rule", ip, "NOK")
                return 1
        except Exception as e:
            ts = datetime.now()
            log.error('[%s] %s %s %s %s',
              ts, "iptables", "add_rule", ip, "EXCEPTION")
            log.error('[%s]', e)
            return e


    def del_rules(self, ips):
        """ Revoking rule for INTERNET access. """
        try:
            rules = 0
            for ip in ips:
                rule = [self.binnary, "-t", self.table, "-D", self.chain, 
                              "-i", self.nic, "-s", ip, "-j", self.jump]
                result = sp.call(rule)
                ts = datetime.now()
                if result == 0:
                    log.error('[%s] %s %s %s %s',
                      ts, "iptables", "del_rule", ip, "OK")
                    rules += 1
                else:
                    log.error('[%s] %s %s %s %s',
                      ts, "iptables", "del_rule", ip, "NOK")

                result = self.del_conntrack(ip)
                if result == 0:
                    log.error('[%s] %s %s %s %s',
                      ts, "iptables", "del_conntrack", ip, "OK")
                else:
                    log.error('[%s] %s %s %s %s',
                      ts, "iptables", "del_conntrack", ip, "NOK")
            return rules
        except Exception as e:
            ts = datetime.now()
            log.error('[%s] %s %s %s',
              ts, "iptables", "del_rule", "EXCEPTION")
            log.error('[%s]', e)
            return e


    def del_conntrack(self, ip):
        """ Destroys established connections from conntrack table. """
        destroy_conn = ["/usr/sbin/conntrack", "-D", "--orig-src", ip]
        result = sp.call(destroy_conn, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
        return result
