#!/usr/bin/env python3

""" Interface for IPTABLES/Netfilter. """

from datetime import datetime
import subprocess as sp

from app import log

class Worker:
    """ Builds and executes IPTABLES/Netfilter rules (add/del)."""

    def test_add_rule(self,ip):
        """ Add Rule (TEST PURPOSES). """
        try:
            r = sp.call(['/sbin/iptables', '-A', 'INPUT', '-i', 'lo', 
                                           '-s', ip, '-p', 'tcp', 
                                           '--dport', '10800', '-j', 'DROP'])
            if r == 0:
                log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "iptables", "test_add_rule", ip, "OK")
                return 0
            else:
                log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "iptables", "test_add_rule", ip, "NOK")
                return 4
        except Exception as e:
            log.error('[%s] %s %s %s %s', datetime.now(), "EVENT", "iptables", "test_add_rule", "EXCEPTION")
            log.error('%s', e)
            return e


    def test_del_rule(self,ips):
        """ Delete rule (TEST PURPOSES). """
        try:
            rules = 0
            for ip in ips:
                r = sp.call(['/sbin/iptables', '-D', 'INPUT', '-i', 'lo', 
                                               '-s', ip, '-p', 'tcp', 
                                               '--dport', '10800', '-j', 'DROP'])
                if r == 0:
                    log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "iptables", "test_del_rule", ip, "OK")
                    rules += 1
                else:
                    log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "iptables", "test_del_rule", ip, "NOK")
            return rules
        except Exception as e:
            log.error('[%s] %s %s %s %s', datetime.now(), "EVENT", "iptables", "test_del_rule", "EXCEPTION")
            log.error('%s', e)
            return e


    def add_rule(self,ip):
        """ Add rule. """
        try:
            r = sp.call(['/sbin/iptables', '-I', 'PREROUTING', '1', '-i', 'eth2', 
                                           '-s', ip, '-p', 'tcp', '--dport', '80', 
                                           '-j', 'DNAT', '--to-destination', '192.168.0.1:3128'])
            if r == 0:
                log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "iptables", "add_rule", ip, "OK")
                return 0
            else:
                log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "iptables", "add_rule", ip, "NOK")
                return 4
        except Exception as e:
            log.error('[%s] %s %s %s %s', datetime.now(), "EVENT", "iptables", "add_rule", "EXCEPTION")
            log.error('%s', e)
            return e


    def del_rule(self,ips):
        """ Delete rule. """
        try:
            rules = 0
            for ip in ips:
                r = sp.call(['/sbin/iptables', '-I', 'PREROUTING', '-i', 'eth2', 
                                               '-s', ip, '-p', 'tcp', '--dport', '80', 
                                               '-j', 'DNAT', '--to-destination', '192.168.0.1:3128'])
                if r == 0:
                    log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "iptables", "del_rule", ip, "OK")
                    rules += 1
                else:
                    log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "iptables", "del_rule", ip, "NOK")
            return rules
        except Exception as e:
            log.error('[%s] %s %s %s %s', datetime.now(), "EVENT", "iptables", "del_rule", "EXCEPTION")
            log.error('%s', e)
            return e
