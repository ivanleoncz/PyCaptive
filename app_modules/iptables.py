
import iptc

class Ruler:

    ip = None
    oper = None

    def __init__(self,ip,oper):
        self.ip = ip
        self.oper = oper

    def add_rule(self):
        try:
            table = iptc.Table(iptc.Table.NAT)
            chain = iptc.Chain(table, "PREROUTING")
            rule = iptc.Rule()
            rule.src = self.ip
            rule.protocol = "tcp"
            rule.in_interface = "eth2"
            match = rule.create_match('tcp')
            match.dport = "80"
            rule.target = rule.create_target("DROP")
            rule.target.to_destination = "192.168.0.1:3128"
            chain.insert_rule(rule)
        except Exception as e:
            print("Exception:", e)
