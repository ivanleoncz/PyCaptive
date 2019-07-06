import re
import yaml

cfg = None
with open('app/pycaptive.yaml', 'r') as f:
    cfg = yaml.load(f)


def iptables(filename):

    print("- IPTABLES: ", filename)

    lines = list()
    # Table [MANGLE]
    #
    #   Packet Flow:
    #
    #   m1 : creates INTERNET chain
    #   m2 : creates PYCAPTIVE chain
    #   m3 : port 80/tcp -> jump to PYCAPTIVE chain
    #   m4 : port 80/udp -> jump to PYCAPTIVE chain
    #   m5 : port 443/tcp -> jump to DROP chain (dropped packets)
    #   m6 : port 443/udp -> jump to DROP chain (dropped packets)
    #   m7 : PYCAPTIVE chain -> move on to NAT table (with mark/tag on Kernel)
    #   m8 : INTERNET chain -> move on to NAT table (Internet (see comments)
    #
    lines.append("*mangle\n")
    lines.append(":PREROUTING ACCEPT [0:0]\n")
    lines.append(":INPUT ACCEPT [0:0]\n")
    lines.append("FORWARD ACCEPT [0:0]\n")
    lines.append(":OUTPUT ACCEPT [0:0]\n")
    lines.append(":POSTROUTING ACCEPT [0:0]\n")
    lines.append("# Internet Access provided after successful PyCaptive login\n")
    lines.append("# adding rule on top of *mangle table, above these chains.\n")
    lines.append("-N INTERNET\n")
    lines.append("-N PYCAPTIVE\n")
    lines.append("-A PREROUTING -i {0} -p tcp -m tcp --dport {1} \
                  -j PYCAPTIVE\n".format(
                      cfg["firewall"]["lan"]["nic"],
                      cfg["firewall"]["services"]["http"]))
    lines.append("-A PREROUTING -i {0} -p tcp -m ucp --dport {1} \
                  -j PYCAPTIVE\n".format(
                      cfg["firewall"]["lan"]["nic"],
                      cfg["firewall"]["services"]["http"]))
    lines.append("-A PREROUTING -i {0} -p tcp -m tcp --dport {1} \
                  -j DROP\n".format(
                      cfg["firewall"]["lan"]["nic"],
                      cfg["firewall"]["services"]["https"]))
    lines.append("-A PREROUTING -i {0} -p tcp -m udp --dport {1} \
                  -j DROP\n".format(
                      cfg["firewall"]["lan"]["nic"],
                      cfg["firewall"]["services"]["https"]))
    lines.append("-A PYCAPTIVE -j MARK --set-mark 1\n")
    lines.append("-A INTERNET -j ACCEPT\n")

    # Table [NAT]
    #
    #   Packet Flow:
    #
    #   n1 : 80/tcp -> NGINX/Gunicorn (PyCaptive)
    #   n2 : 80/udp -> NGINX/Gunicorn (PyCaptive)
    #   n3 : PyCaptive portal accesible after successful login (admin purposes)
    #   n4 : 80/tcp -> Transparent Proxy (check Firewall Mode)
    #   n5 : masquerades LAN IP (WAN IP address as conecction origin)
    #   n6 : external Web Servers -> redirected to Proxy (check Firewall Mode)
    #
    lines.append("*nat\n")
    lines.append(":PREROUTING ACCEPT [0:0]\n")
    lines.append(":INPUT ACCEPT [0:0]\n")
    lines.append(":OUTPUT ACCEPT [0:0]\n")
    lines.append(":POSTROUTING ACCEPT [0:0]\n")
    lines.append("-A PREROUTING -i {0} -p tcp -m tcp -m mark --mark 1 \
                  -j DNAT --to-destination {1}:{2}\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["lan"]["ipaddress"],
                    cfg["firewall"]["services"]["nginx_redir_gunicorn"]))
    lines.append("-A PREROUTING -i {0} -p udp -m udp -m mark --mark 1 \
                  -j DNAT --to-destination {1}:{2}\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["lan"]["ipaddress"],
                    cfg["firewall"]["services"]["nginx_redir_gunicorn"]))
    lines.append("-A PREROUTING -i {0} -s {1} -p tcp -d {2} --dport {3} \
                  -j DNAT --to-destination {4}:{5}\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["lan"]["network"],
                    cfg["firewall"]["lan"]["ipaddress"],
                    cfg["firewall"]["services"]["http"],
                    cfg["firewall"]["lan"]["ipaddress"],
                    cfg["firewall"]["services"]["nginx_redir_gunicorn"]))
    lines.append("-A PREROUTING -i {0} -s {1} -p tcp --dport {2} \
                  -m comment --comment 'Transparent Proxy Access' \
                  -j DNAT --to-destination {3}:{4}\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["lan"]["network"],
                    cfg["firewall"]["services"]["http"],
                    cfg["firewall"]["lan"]["ipaddress"],
                    cfg["firewall"]["services"]["proxy"]))
    lines.append("-A POSTROUTING -o {0} -j MASQUERADE\n".format(
                    cfg["firewall"]["wan"]["nic"]))
    lines.append("-A PREROUTING -i {0} -p tcp --sport {1} \
                  -m comment --comment 'Transparent Proxy Access' \
                  -j REDIRECT --to-port {2}\n".format(
                    cfg["firewall"]["wan"]["nic"],
                    cfg["firewall"]["services"]["http"],
                    cfg["firewall"]["services"]["proxy"]))

    # Table [FILTER]
    #
    #   Packet Flow:
    #
    #   f1  : ACCEPT ICMP traffic (LAN/WAN/LO)
    #   f2  : ACCEPT ESTABLISHED (conntrack) incoming traffic (LAN/WAN/LO)
    #   f3  : ACCEPT localhost traffic
    #   f4  : ACCEPT incoming SSH traffic (LAN)
    #   f5  : ACCEPT incoming DNS/udp traffic (LAN)
    #   f6  : ACCEPT incoming DNS/tcp traffic (LAN)
    #   f7  : ACCEPT incoming DHCP/tcp client traffic (LAN)
    #   f8  : ACCEPT incoming DHCP/tcp server traffic (LAN)
    #   f9  : ACCEPT incoming DNS control via RNDC/udp traffic (LAN)
    #   f10 : ACCEPT incoming DNS control via RNDC/tcp traffic (LAN)
    #   f11 : DROP all incoming connections not listed above (LAN/WAN)
    #   f12 : ACCEPT all outgoing traffic (LAN/WAN/LO)
    #
    lines.append("*filter\n")
    lines.append(":INPUT ACCEPT [0:0]\n")
    lines.append(":FORWARD ACCEPT [0:0]\n")
    lines.append(":OUTPUT ACCEPT [0:0]\n")
    lines.append("-A INPUT -p icmp -m conntrack \
                  --ctstate NEW,ESTABLISHED,RELATED --icmp-type 8 -j ACCEPT\n")
    lines.append("-A INPUT -m conntrack \
                  --ctstate RELATED,ESTABLISHED -j ACCEPT\n")
    lines.append("-A INPUT -i lo -j ACCEPT\n")
    lines.append("-A INPUT -i {0} -p tcp --dport {1} \
                  -j ACCEPT\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["services"]["ssh"]))
    lines.append("-A INPUT -i {0} -p udp --dport {1} \
                  -j ACCEPT\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["services"]["dns"]))
    lines.append("-A INPUT -i {0} -p tcp --dport {1} \
                  -j ACCEPT\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["services"]["dns"]))
    lines.append("-A INPUT -i {0} -p udp --dport {1} --sport {2} \
                  -j ACCEPT\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["services"]["dhcp_server"],
                    cfg["firewall"]["services"]["dhcp_client"]))
    lines.append("-A INPUT -i {0} -p udp --dport {1} --sport {2} \
                  -j ACCEPT\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["services"]["dhcp_client"],
                    cfg["firewall"]["services"]["dhcp_server"]))
    lines.append("-A INPUT -i {0} -p udp --dport {1} \
                  -j ACCEPT\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["services"]["dns_rndc"]))
    lines.append("-A INPUT -i {0} -p tcp --dport {1} \
                  -j ACCEPT\n".format(
                    cfg["firewall"]["lan"]["nic"],
                    cfg["firewall"]["services"]["dns_rndc"]))
    lines.append("-A INPUT -j REJECT\n")
    lines.append("-A OUTPUT -j ACCEPT\n")

    with open(filename, "w") as f:
        for line in lines:
            if "Transparent Proxy" in line:
                if cfg["firewall"]["general"]["operation_mode"] == 2:
                    f.write(re.sub(' +', ' ', line))
            else:
                f.write(re.sub(' +', ' ', line))


def nginx(filename):

    print("- NGINX: ", filename)

    lines = list()
    lines.append("server {\n")
    lines.append("  listen {0}:{1};\n".format(
                cfg['firewall']['lan']['ipaddress'],
                cfg['firewall']['services']['nginx_redir_gunicorn']))
    lines.append("  server_name ~^(www\.)?(?<domain>.+)$;\n")
    lines.append("  return 301 $scheme://{0}:{1}/login;\n\n".format(
                cfg['firewall']['lan']['ipaddress'],
                cfg['firewall']['services']['nginx_gunicorn']))
    lines.append("  access_log /var/log/nginx/redirect_PyCaptive.access.log;\n")
    lines.append("  error_log /var/log/nginx/redirect_PyCaptive.error.log;\n}")

    lines.append("\n\nserver {\n")
    lines.append("  listen {0}:{1};\n\n".format(
                cfg['firewall']['lan']['ipaddress'],
                cfg['firewall']['services']["nginx_gunicorn"]))
    lines.append("  location / {\n")
    lines.append("     include proxy_params;\n")
    lines.append("     proxy_pass http://unix:/opt/PyCaptive/wsgi.sock;\n")
    lines.append("  }\n\n")
    lines.append("  access_log /var/log/nginx/PyCaptive.access.log;\n")
    lines.append("  error_log /var/log/nginx/PyCaptive.error.log;\n\n}")

    with open(filename, "w") as f:
        for line in lines:
            f.write(re.sub(' +', ' ', line))


def sudoers(filename):

    print("- SUDOERS: ", filename)

    lines = list()
    lines.append("pycaptive ALL=(root:root) NOPASSWD:/sbin/iptables\n")
    lines.append("pycaptive ALL=(root:root) NOPASSWD:/usr/sbin/conntrack\n")

    with open(filename, "w") as f:
        for line in lines:
            f.write(re.sub(' +', ' ', line))


def supervisor(filename):

    print("- SUPERVISOR: ", filename)

    lines = list()
    lines.append("[program:pycaptive]\n")
    lines.append("command = gunicorn -n gnc_master \
                  -u gunicorn -g gunicorn -b unix:/opt/PyCaptive/wsgi.sock \
                  -w 2 --pythonpath /opt/PyCaptive app:app\n")
    lines.append("autostart = true\n")
    lines.append("autorestart = true\n")
    lines.append("stderr_logfile = /var/log/supervisor/pycaptive.err.log\n")
    lines.append("stdout_logfile = /var/log/supervisor/pycaptive.out.log\n")



    with open(filename, "w") as f:
        for line in lines:
            f.write(re.sub(' +', ' ', line))


def logrotate(filename):

    print("- LOGROTATE: ", filename)

    lines = list()
    lines.append("/var/log/pycaptive/*.log {\n")
    lines.append("        monthly\n")
    lines.append("        missingok\n")
    lines.append("        rotate 12\n")
    lines.append("        compress\n")
    lines.append("        delaycompress\n")
    lines.append("        notifempty\n")
    lines.append("        postrotate\n")
    lines.append("                supervisorctl reload\n")
    lines.append("        endscript\n")
    lines.append("}")

    with open(filename, "w") as f:
        for line in lines:
            f.write(re.sub(' +', ' ', line))


print("Building configuration files: ")
iptables("configurations/rules.v4")
nginx("configurations/pycaptive_site")
sudoers("configurations/pycaptive_sudo")
supervisor("configurations/pycaptive.conf")
logrotate("configurations/pycaptive_logrotate")
