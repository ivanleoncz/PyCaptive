#!/usr/bin/env python3

""" Interface for IPTABLES/Netfilter. """

import subprocess as sp

class Worker:
    """ IPTABLES/Netfilter jobs."""

    def test_add_rule(self,ip):
        """ Test Purposes: Add Rule """
        try:
            print("IPTABLES: test_add_rule() has been called.")
            r = sp.call(['/sbin/iptables', '-A', 'INPUT', '-i', 'lo', 
                                                '-s', ip, '-p', 'tcp', '--dport', '10800', '-j', 'DROP'])
            if r == 0:
                print("IPTABLES: firewall rule has been ADDED.")
                return 0
            else:
                print("IPTABLES: fail to ADD firewall rule.")
                return 1
        except Exception as e:
            return "ERROR: %s" % e


    def test_del_rule(self,ips):
        """ Test Purposes; Delete Rules """
        try:
            print("IPTABLES: test_add_rule() has been called.")
            rules = 0
            for ip in ips:
                r = sp.call(['/sbin/iptables', '-D', 'INPUT', '-i', 'lo', 
                                                    '-s', ip, '-p', 'tcp', '--dport', '10800', '-j', 'DROP'])
                if r == 0:
                    print("IPTABLES: firewall rule has been DELETED.")
                    rules += 1
                else:
                    print("IPTABLES: fail to DELETE firewall rule.")
            return rules
        except Exception as e:
            return "ERROR: %s" % e


    def add_rule(self,ip):
        """ Adding rule. """
        try:
            print("IPTABLES: test_add_rule() has been called.")
            r = sp.call(['/sbin/iptables', '-I', 'PREROUTING', '1', '-i', 'eth2', 
                                                          '-s', ip, '-p', 'tcp', '--dport', '80', 
                                                          '-j', 'DNAT', '--to-destination', '192.168.0.1:3128'])
            if r == 0:
                print("IPTABLES: firewall rule has been ADDED.")
                return 0
            else:
                print("IPTABLES: fail to ADD firewall rule.")
                return 1
        except Exception as e:
            return "ERROR: %s" % e


    def del_rule(self,ips):
        """ Deleting rule. """
        try:
            print("IPTABLES: test_add_rule() has been called.")
            rules = 0
            for ip in ips:
                r = sp.call(['/sbin/iptables', '-I', 'PREROUTING', '-i', 'eth2', 
                                                         '-s', ip, '-p', 'tcp', '--dport', '80', 
                                                         '-j', 'DNAT', '--to-destination', '192.168.0.1:3128'])
                if r == 0:
                    print("IPTABLES: firewall rule has been DELETED.")
                    rules += 1
                else:
                    print("IPTABLES: fail to DELETE firewall rule.")
            return rules
        except Exception as e:
            return "ERROR: %s" % e
