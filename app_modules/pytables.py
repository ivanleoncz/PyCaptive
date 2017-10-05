
import iptc

class PyTables:

    ip = None

    def __init__(self):

    def add_rule(ip,op):
        rule = iptc.Rule()
        rule.src = ip
        rule.protocol = "tcp"
        rule.target = iptc.Target(rule, "DNAT")
        chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "INPUT")
        if op == "add":
            try:
                chain.insert_rule(rule)
                return "{"add_ip":"ok"}"
            except:
                return "{"add_ip":"nok"}"
        elif op == "del":
            try:
                chain.delete_rule(rule)
                return "{"del_ip":"ok"}"
            except:
                return "{"del_ip":"nok"}"
        else:
            return "Wrong option!"


