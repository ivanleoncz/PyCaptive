

from app import iptables_dict as d

__author__ = "@ivanleoncz"

import subprocess as sp


class Worker:
    """ A base class for IPTABLES/Netfilter jobs, supporting PyCaptive on
        allowing/prohibiting Internet access for its clients, through their
        IP addresses.
    """

    def add_rule(self, ip):
        """
        Allowing Internet access to an IP address

        Parameters
        ----------
        ip : string
             IP address provided via client request to PyCaptive.

        Returns
        -------
        integer
             if 0: rule successfully deleted
             else: error while processing command

        """
        rule = [
                d.get("IPTABLES"),
                "-t", d.get("TABLE"),
                "-I", d.get("CHAIN"),
                "-i", d.get("LAN"),
                "-s", ip,
                "-m", "comment", "--comment", d.get("COMMENT"),
                "-j", d.get("JUMP")
                ]
        try:
            result = sp.call(rule)
            if result == 0:
                log.info('%s %s %s %s', "iptables", "add_rule", "OK", ip)
            else:
                log.error('%s %s %s %s', "iptables", "add_rule", "NOK", ip)
            return result
        except Exception as e:
            log.critical('%s %s %s %s', "iptables", "add_rule", "EXCEPTION", ip)
            log.critical('%s', e)
            return e


    def del_rules(self, ips):
        """
        Deleting rules that grant Internet access to a list of IPs and
        destroying connections established for such IPs.

        See del_conntrack() for more info.

        Parameters
        ----------
        ips : list
              IP addressess provided via scheduler (APScheduler).

        Returns
        -------
        integer
              Number of deleted rules.

        """
        try:
            rules = 0
            for ip in ips:
                # deleting rule
                rule = [
                        d.get("IPTABLES"),
                        "-t", d.get("TABLE"),
                        "-D", d.get("CHAIN"),
                        "-i", d.get("LAN"),
                        "-s", ip,
                        "-m", "comment", "--comment", d.get("COMMENT"),
                        "-j", d.get("JUMP")
                        ]
                result = sp.call(rule)
                if result == 0:
                    log.info('%s %s %s %s', "iptables", "del_rules", "OK", ip)
                    rules += 1
                else:
                    log.error('%s %s %s %s', "iptables", "del_rules", "NOK", ip)
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
        """
        Destroys established connections from conntrack table for a specified
        IP address.

        This action is complementary to del_rules() method, in order to insure
        that no connection is persisting between a PyCaptive client and a
        remote IP address.

        See del_rules() for more info.

        Parameters
        ----------
        ip : string
             IP address provided via del_rules() method.

        Returns
        -------
        integer
             if 0: rule successfully deleted
             else: error while processing command

        """
        destroy_conn = [d.get("CONNTRACK"), "-D", "--orig-src", ip]
        result = sp.call(destroy_conn, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
        if result == 0:
            log.info('%s %s %s %s', "iptables", "del_conntrack", "OK", ip)
        else:
            log.error('%s %s %s %s', "iptables", "del_conntrack", "NOK", ip)
        return result
