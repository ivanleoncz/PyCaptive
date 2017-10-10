
""" Interface for IPTABLES/Netfilter. """

import iptc

class Ruler:
    """ IPTABLES/Netfilter jobs."""

    ip = None

    def __init__(self,ip):
        self.ip = ip

    def add_rule(self):
        """ Adding rule. """
        try:
            table = iptc.Table(iptc.Table.NAT)
            chain = iptc.Chain(table, "PREROUTING")
            rule = iptc.Rule()
            rule.src = self.ip
            rule.protocol = "tcp"
            rule.in_interface = "eth2"
            rule.target = rule.create_target("DROP")
            rule.target.to_destination = "192.168.0.1:3128"
            match = rule.create_match('tcp')
            match.dport = "80"
            chain.insert_rule(rule)
            return "ok"
        except Exception as e:
            return e

    def del_rule(self):
        """ Deleting rule. """
        try:
            table = iptc.Table(iptc.Table.NAT)
            chain = iptc.Chain(table, "PREROUTING")
            for rule in chain.rules:
                if rule.src == self.ip:
                    chain.delete_rule(rule)
                    break
            return "ok"
        except Exception as e:
            return e
