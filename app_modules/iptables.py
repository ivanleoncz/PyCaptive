#!/usr/bin/env python3

""" Interface for IPTABLES/Netfilter. 
    
    Return Codes:

    0x0000 - Successful
    0x0fw1 - fail to add firewall rule
"""

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
            return "0x0000"
        except Exception as e:
            print("ERROR: fail TO ADD firewall rule:", e)
            return "0x0fw1"

    def test_del_rule(self,ips):
        """ Test Rule (del). """
        try:
            table = iptc.Table(iptc.Table.FILTER)
            chain = iptc.Chain(table, "INPUT")
            table.autocommit = False
            deleted_rules = 0
            for ip in ips: 
                for rule in chain.rules:
                    if rule.src == ip and rule.in_interface is not None and "lo" in rule.in_interface:
                        for match in rule.matches:
                            if match.dport == "9999":
                                chain.delete_rule(rule)
                                deleted_rules += 1
            table.commit()
            table.autocommit = True
            return deleted_rules
        except Exception as e:
            print("ERROR: fail TO DEL firewall rule:",e)
            return "0x0fw1"

    # ---> need review
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
            return "0x0000"
        except Exception:
            print("ERROR: fail TO ADD firewall rule...")
            return "0x0fw1"

    # ---> need review
    def del_rule(self,ip):
        """ Deleting rule. """
        try:
            table = iptc.Table(iptc.Table.NAT)
            chain = iptc.Chain(table, "PREROUTING")
            for rule in chain.rules:
                if rule.src == ip:
                    chain.delete_rule(rule)
                    break
            return "0x0000"
        except Exception:
            print("ERROR: fail TO DEL firewall rule...")
            return "0x0fw1"
