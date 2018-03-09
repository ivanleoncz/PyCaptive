#!/usr/bin/env python3

""" Interface for IPTABLES/Netfilter. """

from datetime import datetime
from app import log

__author__ = "@ivanleoncz"

import subprocess as sp


class Worker:
    """ Builds and executes IPTABLES/Netfilter rules (add/del)."""

    # Depending on the setup of your Firewall/Proxy, 
    # here you can customize the params for the rules.
    binnary = "/sbin/iptables"
    table   = "mangle"
    chain   = "PREROUTING"
    nic     = "eth2"
    jump    = "INTERNET"

    def add_rule(self,ip):
        """ Add rule. """
        rule = [self.binnary, "-t",self.table, "-I", self.chain,
                              "-i",self.nic, "-s",ip, "-j",self.jump]
        try:
            result = sp.call(rule)
            ts = datetime.now()
            if result == 0:
                log.error('[%s] %s %s %s %s %s', 
                           ts, "EVENT", "iptables", "add_rule", ip, "OK")
                return 0
            else:
                log.error('[%s] %s %s %s %s %s', 
                           ts, "EVENT", "iptables", "add_rule", ip, "NOK")
                return 4
        except Exception as e:
            ts = datetime.now()
            log.error('[%s] %s %s %s %s', 
                       ts, "EVENT", "iptables", "add_rule", "EXCEPTION")
            log.error('[%s]', e)
            return e


    def del_rule(self,ips):
        """ Delete rule. """
        try:
            rules = 0
            for ip in ips:
                rule = [self.binnary, "-t", self.table, "-D", self.chain, 
                                      "-i", self.nic, "-s", ip, "-j", self.jump]
                result = sp.call(rule)
                ts = datetime.now()
                if result == 0:
                    log.error('[%s] %s %s %s %s %s', 
                               ts, "EVENT", "iptables", "del_rule", ip, "OK")
                    rules += 1
                else:
                    log.error('[%s] %s %s %s %s %s', 
                               ts, "EVENT", "iptables", "del_rule", ip, "NOK")

                result = del_conntrack(ip)
                if result == 0:
                    log.error('[%s] %s %s %s %s %s', 
                               ts, "EVENT", "iptables", "del_conntrack", ip, "OK")
                else:
                    log.error('[%s] %s %s %s %s %s', 
                               ts, "EVENT", "iptables", "del_conntrack", ip, "NOK")

            return rules
        except Exception as e:
            ts = datetime.now()
            log.error('[%s] %s %s %s %s', 
                       ts, "EVENT", "iptables", "del_rule", "EXCEPTION")
            log.error('[%s]', e)
            return e

    def del_conntrack(self,ip):
        """ Wipe established connections from conntrack table. """
        wipe_connection = ["/usr/sbin/conntrack", "-D", "--orig-src", ip] 
        result = sp.call(wipe_connection)
        return result
