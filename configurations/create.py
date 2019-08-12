import os
import re
import yaml


cfg = None

pycaptive_dir = os.path.abspath('..')
pycaptive_file = os.path.join(pycaptive_dir, "app/pycaptive.yaml")
with open(pycaptive_file, 'r') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


def create_conf_iptables():
    """ Creates Netfilter/IPTABLES configuration for PyCaptive. """

    filename = "rules.v4"
    l = list()

    # *** Table [MANGLE] ***
    l.append("# BEGIN\n\n")
    l.append("*mangle\n")
    l.append(":PREROUTING ACCEPT [0:0]\n")
    l.append(":INPUT ACCEPT [0:0]\n")
    l.append("FORWARD ACCEPT [0:0]\n")
    l.append(":OUTPUT ACCEPT [0:0]\n")
    l.append(":POSTROUTING ACCEPT [0:0]\n\n")
    l.append("# Creates INTERNET chain\n")
    l.append("-N INTERNET\n")
    l.append("# Creates PYCAPTIVE chain\n")
    l.append("-N PYCAPTIVE\n\n")
    l.append("# [Route => LAN]\n")
    l.append("#\n# * REDIRECT traffic with port 80/TCP as \
        target, to PYCAPTIVE chain\n")
    l.append("-A PREROUTING -i {} -p tcp -m tcp --dport {} \
        -j PYCAPTIVE\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["services"]["http"]))
    l.append("# * REDIRECT traffic with port 80/UDP as target,\
            to PYCAPTIVE chain\n")
    l.append("-A PREROUTING -i {} -p tcp -m ucp --dport {} \
        -j PYCAPTIVE\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["services"]["http"]))
    l.append("# * DROP traffic with port 443/TCP as target\n")
    l.append("-A PREROUTING -i {} -p tcp -m tcp --dport {} \
        -j DROP\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["services"]["https"]))
    l.append("# * DROP traffic with port 443/UDP as target\n")
    l.append("-A PREROUTING -i {} -p udp -m udp --dport {} \
        -j DROP\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["services"]["https"]))
    l.append("# * MARK packets with PYCAPTIVE chain as target \
            (processing continues on NAT table...)\n")
    l.append("-A PYCAPTIVE -i {} -j MARK --set-mark 1\n".format(
        cfg["firewall"]["lan"]["nic"]))
    l.append("# * ACCEPT received packets\n")
    l.append("# => Successful logins, generate rules on top of MANGLE table, ")
    l.append("one per IP address.\n")
    l.append("# => All rules, REDIRECT traffic to INTERNET chain, which ")
    l.append("gives Free Internet Access for IPs (users) which have")
    l.append("successfuly authenticated.\n")
    l.append("-A INTERNET -i {} -j ACCEPT\n\n".format(
        cfg["firewall"]["lan"]["nic"]))

    # *** Table [NAT] ***
    l.append("\n*nat\n")
    l.append(":PREROUTING ACCEPT [0:0]\n")
    l.append(":INPUT ACCEPT [0:0]\n")
    l.append(":OUTPUT ACCEPT [0:0]\n")
    l.append(":POSTROUTING ACCEPT [0:0]\n\n")
    l.append("# [Route NAT => LAN]\n#\n")
    l.append("# * REDIRECT 'marked' packets with port 80/TCP as target, ")
    l.append("to NGINX (Redirect Gunicorn/PyCaptive)\n")
    l.append("-A PREROUTING -i {} -p tcp -m tcp -m mark --mark 1 -j DNAT \
        --to-destination {}:{}\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["lan"]["ipaddress"],
        cfg["firewall"]["services"]["nginx_redir_gunicorn"]))
    l.append("# * REDIRECT 'marked' packets with port 80/UDP as target ")
    l.append("to NGINX (Redirect Gunicorn/PyCaptive)\n")
    l.append("-A PREROUTING -i {} -p udp -m udp -m mark --mark 1 -j DNAT \
        --to-destination {}:{}\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["lan"]["ipaddress"],
        cfg["firewall"]["services"]["nginx_redir_gunicorn"]))
    l.append("# * REDIRECT traffic with port 80/UDP as target, to NGINX ")
    l.append("(Redirect Gunicorn/PyCaptive)\n")
    l.append("# => It ensures that PyCaptive is still accessible for ")
    l.append("Administration purposes (not implemented yet..), ")
    l.append("for an authenticated IP (user).\n")
    l.append("-A PREROUTING -i {} -s {} -p tcp -d {} --dport {} -j DNAT \
        --to-destination {}:{}\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["lan"]["network"],
        cfg["firewall"]["lan"]["ipaddress"],
        cfg["firewall"]["services"]["http"],
        cfg["firewall"]["lan"]["ipaddress"],
        cfg["firewall"]["services"]["nginx_redir_gunicorn"]))
    l.append("# * REDIRECT traffic with port 80/TCP as target, to \
            Transparent Proxy (check operation_mode on pycaptive.yaml)\n")
    l.append("-A PREROUTING -i {} -s {} -p tcp --dport {} -m comment --comment \
        'Transparent Proxy' -j DNAT --to-destination {}:{}\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["lan"]["network"],
        cfg["firewall"]["services"]["http"],
        cfg["firewall"]["lan"]["ipaddress"],
        cfg["firewall"]["services"]["proxy"]))
    l.append("# * MASQUERADE client IP with WAN IP address, for the remote ")
    l.append("Web Server.\n")
    l.append("-A POSTROUTING -o {} -j MASQUERADE\n".format(
        cfg["firewall"]["wan"]["nic"]))
    l.append("# * REDIRECT traffic from External Web Servers to \
            Transparent Proxy (check operation_mode on pycaptive.yaml)\n")
    l.append("-A PREROUTING -i {} -p tcp --sport {} -m comment --comment \
        'Transparent Proxy' -j REDIRECT --to-port {}".format(
        cfg["firewall"]["wan"]["nic"],
        cfg["firewall"]["services"]["http"],
        cfg["firewall"]["services"]["proxy"]))

    # *** Table [FILTER] ***
    l.append("\n\n*filter\n")
    l.append(":INPUT ACCEPT [0:0]\n")
    l.append(":FORWARD ACCEPT [0:0]\n")
    l.append(":OUTPUT ACCEPT [0:0]\n\n")
    l.append("# [Input => ALL INTERFACES]\n#\n")
    l.append("# * ACCEPT ICMP traffic!\n")
    l.append("-A INPUT -p icmp -m conntrack \
        --ctstate NEW,ESTABLISHED,RELATED --icmp-type 8 -j ACCEPT\n")
    l.append("# * ACCEPT traffic RELATED and ESTABLISHED (conntrack)\n")
    l.append("-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT\n\n")

    l.append("# [Input => Loopback/Localhost]\n#\n")
    l.append("# * ACCEPT everything!\n")
    l.append("-A INPUT -i lo -j ACCEPT\n\n")

    l.append("# [Input => LAN]\n#\n# * ACCEPT SSH\n")
    l.append("-A INPUT -i {} -p tcp --dport {} -j ACCEPT\n".format(
        cfg["firewall"]["lan"]["nic"], cfg["firewall"]["services"]["ssh"]))
    l.append("# * ACCEPT DNS (UDP)\n")
    l.append("-A INPUT -i {} -p udp --dport {} -j ACCEPT\n".format(
        cfg["firewall"]["lan"]["nic"], cfg["firewall"]["services"]["dns"]))
    l.append("# * ACCEPT DNS (TCP)\n")
    l.append("-A INPUT -i {} -p tcp --dport {} -j ACCEPT\n".format(
        cfg["firewall"]["lan"]["nic"], cfg["firewall"]["services"]["dns"]))
    l.append("# * ACCEPT DHCP (UDP) - client traffic\n")
    l.append("-A INPUT -i {} -p udp --dport {} --sport {} -j ACCEPT\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["services"]["dhcp_server"],
        cfg["firewall"]["services"]["dhcp_client"]))
    l.append("# * ACCEPT DHCP (UDP) - server traffic\n")
    l.append("-A INPUT -i {} -p udp --dport {} --sport {} -j ACCEPT\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["services"]["dhcp_client"],
        cfg["firewall"]["services"]["dhcp_server"]))
    l.append("# * ACCEPT Remote Control of BIND DNS Server via RNDC (UDP)\n")
    l.append("-A INPUT -i {} -p udp --dport {} -j ACCEPT\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["services"]["dns_rndc"]))
    l.append("# * ACCEPT Remote Control of BIND DNS Server via RNDC (TCP)\n")
    l.append("-A INPUT -i {} -p tcp --dport {} -j ACCEPT\n\n".format(
        cfg["firewall"]["lan"]["nic"],
        cfg["firewall"]["services"]["dns_rndc"]))

    l.append("# [Input => ALL INTERFACES]\n#\n# * REJECT everything, \
            thats is not listed above!\n")
    l.append("-A INPUT -j REJECT\n\n")

    l.append("# [Output <= ALL INTERFACES]\n#\n# * ACCEPT everything!\n")
    l.append("-A OUTPUT -j ACCEPT\n\n")

    l.append("# END")

    with open(filename, "w") as f:
        for line in l:
            if "Transparent Proxy" in line:
                if cfg["firewall"]["general"]["operation_mode"] == 2:
                    f.write(re.sub(' +', ' ', line))
            else:
                f.write(re.sub(' +', ' ', line))


def create_conf_nginx():
    """ Creates NGINX site configuration. """

    filename = "pycaptive_nginx"
    l = list()

    # Server Block: redirect request to the Server Block below
    #
    # That is one of the triggers which Android and iOS devices
    # use in order to detect Captive Portals.
    #
    l.append("server {\n")
    l.append("  listen {}:{};\n".format(
        cfg['firewall']['lan']['ipaddress'],
        cfg['firewall']['services']['nginx_redir_gunicorn']))
    l.append("  server_name ~^(www\.)?(?<domain>.+)$;\n")
    l.append("  return 301 $scheme://{}:{}/login;\n\n".format(
        cfg['firewall']['lan']['ipaddress'],
        cfg['firewall']['services']['nginx_gunicorn']))
    l.append("  access_log /var/log/nginx/redirect_pycaptive.access.log;\n")
    l.append("  error_log /var/log/nginx/redirect_pycaptive.error.log;\n}\n\n")

    # Server Block: receives request from the Server Block above
    #
    # Here, the request is transmited to Gunicorn, including the default
    # Proxy Parameters defined on the Nginx installed on the machine.
    #
    l.append("server {\n")
    l.append("  listen {}:{};\n\n".format(
        cfg['firewall']['lan']['ipaddress'],
        cfg['firewall']['services']["nginx_gunicorn"]))
    l.append("  location /login {\n")
    l.append("     include proxy_params;\n")
    l.append("     proxy_pass http://unix:/opt/pycaptive/wsgi.sock;\n")
    l.append("  }\n\n")
    l.append("  access_log /var/log/nginx/pycaptive.access.log;\n")
    l.append("  error_log /var/log/nginx/pycaptive.error.log;\n}")

    with open(filename, "w") as f:
        for line in l:
            f.write(re.sub(' +', ' ', line))


def create_conf_sudoers():
    """ Creates SUDO configuration for 'pycaptive' user. """

    filename = "pycaptive_sudo"
    l = list()

    l.append("pycaptive ALL=(root:root) NOPASSWD:/sbin/iptables\n")
    l.append("pycaptive ALL=(root:root) NOPASSWD:/usr/sbin/conntrack\n")

    with open(filename, "w") as f:
        for line in l:
            f.write(re.sub(' +', ' ', line))


def create_conf_supervisor():
    """ Creates Supervisor configuration for 'pycaptive' user. """

    filename = "pycaptive.conf"
    l = list()

    l.append("[program:pycaptive]\n")
    l.append("command = gunicorn -n gnc_master -u gunicorn -g gunicorn \
        -b unix:/opt/pycaptive/wsgi.sock \
        -w 2 --pythonpath /opt/pycaptive app:app\n")
    l.append("autostart = true\n")
    l.append("autorestart = true\n")
    l.append("stderr_logfile = /var/log/supervisor/pycaptive.err.log\n")
    l.append("stdout_logfile = /var/log/supervisor/pycaptive.out.log\n")

    with open(filename, "w") as f:
        for line in l:
            f.write(re.sub(' +', ' ', line))


def create_conf_logrotate():
    """ Creates logrotation configuration for PyCaptive logs. """

    filename = "pycaptive_logrotate"
    l = list()

    l.append("/var/log/pycaptive/*.log {\n")
    l.append("      monthly\n")
    l.append("      missingok\n")
    l.append("      rotate 12\n")
    l.append("      compress\n")
    l.append("      delaycompress\n")
    l.append("      notifempty\n")
    l.append("      postrotate\n")
    l.append("          supervisorctl reload\n")
    l.append("      endscript\n")
    l.append("}")

    with open(filename, "w") as f:
        for line in l:
            f.write(re.sub(' +', ' ', line))


print("Building configuration files... ")
create_conf_iptables()
create_conf_nginx()
create_conf_sudoers()
create_conf_supervisor()
create_conf_logrotate()
print("Done")
