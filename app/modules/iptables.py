#!/usr/bin/python3
""" Allowing/prohibiting traffic based on user authentication/session.

This module is responsible for granting/revoking access to network traffic
via Firewall rules (IPTABLES/Netfilter), for the IP addresses from
the devices used on successful authentication processes.

NOTICE: use the class variables, in order to customize the paramaters used on
the Firewall rules, depending on the setup that you have for your
Firewall/Proxy. 

For example, the setup considered here is:
a GNU/Linux Router (with Squid3 Proxy in Transparent Mode), with some
specific chains (IPTABLES), all processed on mangle table.

Feel free to implement this module, according to your needs.

"""

from datetime import datetime
from app import log

__author__ = "@ivanleoncz"

import subprocess as sp


class Worker:
    """ IPTABLES/Netfilter rules for allowing/prohibiting network traffic. """

    binnary = "/sbin/iptables"
    table   = "mangle"
    chain   = "PREROUTING"
    nic     = "eth2"
    jump    = "INTERNET"

    def add_rule(self, ip):
        """ Allowing network traffic. """
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
        """ Revoking rule for network traffic. """
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
        result = sp.call(destroy_conn)
        return result
