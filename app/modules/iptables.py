#!/usr/bin/env python3

""" Interface for IPTABLES/Netfilter. """

import iptc

class Worker:
    """ IPTABLES/Netfilter jobs."""

    def test_add_rule(self,ip):
        """ Test Rule (add). """
        try:
            table = iptc.Table(iptc.Table.FILTER)
            chain = iptc.Chain(table, "INPUT")
            rule = iptc.Rule()
            rule.src = ip
            rule.protocol = "tcp"
            rule.in_interface =  "lo"
            rule.target = rule.create_target("DROP")
            match = rule.create_match("tcp")
            match.dport = "9999"
            chain.insert_rule(rule)
            return 0
        except Exception as e:
            return "ERROR: %s" % e

    def test_del_rule(self,ips):
        """ Test Rule (del). """
        try:
            table = iptc.Table(iptc.Table.FILTER)
            chain = iptc.Chain(table, "INPUT")
            table.autocommit = False
            deleted_rules = 0
            for ip in ips:
                for rule in chain.rules:
                    ip_rule = rule.src.split('/')[0]
                    if ip_rule == ip and rule.in_interface is not None and rule.in_interface == "lo":
                        for match in rule.matches:
                            if match.dport == "9999":
                                chain.delete_rule(rule)
                                deleted_rules += 1
            table.commit()
            table.autocommit = True
            return deleted_rules
        except Exception as e:
            return "ERROR: %s" % e

    # ---> needs review...
    def add_rule(self,ip):
        """ Adding rule. """
        try:
            table = iptc.Table(iptc.Table.NAT)
            chain = iptc.Chain(table, "PREROUTING")
            rule = iptc.Rule()
            rule.src = ip
            rule.protocol = "tcp"
            rule.in_interface = "eth2"
            rule.target = rule.create_target("DROP")
            rule.target.to_destination = "192.168.0.1:3128"
            match = rule.create_match('tcp')
            match.dport = "80"
            chain.insert_rule(rule)
            return 0
        except Exception as e:
            return "ERROR: %s" % e

    # ---> needs review...
    def del_rule(self,ips):
        """ Deleting rule. """
        try:
            table = iptc.Table(iptc.Table.NAT)
            chain = iptc.Chain(table, "PREROUTING")
            for rule in chain.rules:
                if rule.src == ip:
                    chain.delete_rule(rule)
                    break
            return 0
        except Exception as e:
            return "ERROR: %s" % e
