""" Allowing/prohibiting INTERNET access based on IP addresses. """


from datetime import datetime

from app import log, IPTABLES, TABLE, LAN, CHAIN, JUMP

__author__ = "@ivanleoncz"

import subprocess as sp


class Worker:
    """ IPTABLES/Netfilter rules for allowing/prohibiting INTERNET access. """


    def add_rule(self, ip):
        """ Allowing INTERNET access. """
        rule = [IPTABLES, "-t", TABLE, "-I", CHAIN, "-i", LAN,
                "-s", ip, "-j", JUMP]
        try:
            result = sp.call(rule)
            if result == 0:
                log.info('%s %s %s %s',
                         "iptables", "add_rule", "OK", ip)
                return 0
            else:
                log.error('%s %s %s %s',
                          "iptables", "add_rule", "NOK", ip)
                return 1
        except Exception as e:
            log.critical('%s %s %s %s',
                         "iptables", "add_rule", "EXCEPTION", ip)
            log.critical('%s', e)
            return e


    def del_rules(self, ips):
        """ Revoking rule for INTERNET access. """
        try:
            rules = 0
            for ip in ips:
                # deleting rule
                rule = [IPTABLES, "-t", TABLE, "-D", CHAIN, "-i", LAN,
                        "-s", ip, "-j", JUMP]
                result = sp.call(rule)
                if result == 0:
                    log.info('%s %s %s %s',
                              "iptables", "del_rules", "OK", ip)
                    rules += 1
                else:
                    log.error('%s %s %s %s',
                              "iptables", "del_rules", "NOK", ip)
                # destroying connection
                result = self.del_conntrack(ip)
                if result == 0:
                    log.info('%s %s %s %s',
                             "del_rules", "OK", "CONNECTIONS_DESTROYED", ip)
                else:
                    log.error('%s %s %s %s',
                             "del_rules", "NOK", "CONNECTIONS_PERSISTING", ip)
            return rules
        except Exception as e:
            log.critical('%s %s %s', "iptables", "del_rule", "EXCEPTION")
            log.critical('%s', e)
            return e


    def del_conntrack(self, ip):
        """ Destroys established connections from conntrack table. """
        destroy_conn = ["/usr/sbin/conntrack", "-D", "--orig-src", ip]
        result = sp.call(destroy_conn, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
        if result == 0:
            log.info('%s %s %s %s', "iptables", "del_conntrack", "OK", ip)
        else:
            log.error('%s %s %s %s', "iptables", "del_conntrack", "NOK", ip)
        return result
