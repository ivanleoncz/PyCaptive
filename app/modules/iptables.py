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
                # deleting rule
                rule = [IPTABLES, "-t", TABLE, "-D", CHAIN, "-i", LAN,
                        "-s", ip, "-j", JUMP]
                result = sp.call(rule)
                ts = datetime.now()
                if result == 0:
                    log.error('[%s] %s %s %s %s',
                      ts, "iptables", "del_rule", ip, "OK")
                    rules += 1
                else:
                    log.error('[%s] %s %s %s %s',
                      ts, "iptables", "del_rule", ip, "NOK")
                # destroying connection
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
            log.error('[%s] %s %s %s', ts, "iptables", "del_rule", "EXCEPTION")
            log.error('[%s]', e)
            return e


    def del_conntrack(self, ip):
        """ Destroys established connections from conntrack table. """
        destroy_conn = ["/usr/sbin/conntrack", "-D", "--orig-src", ip]
        result = sp.call(destroy_conn, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
        return result
