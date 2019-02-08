from app import app

def iptables():

    FILE="deploy/iptables/rules.v4"

    print("- IPTABLES: ", FILE)

    # Table [MANGLE]
    #
    #   Packet Flow:
    #
    #   m1 : creates INTERNET chain
    #   m2 : creates PYCAPTIVE chain
    #   m3 : port 80/tcp (HTTP) as destination -> jumped to PYCAPTIVE chain (see "m7")
    #   m4 : port 80/udp (HTTP) as destination -> jumped to PYCAPTIVE chain (see "m7")
    #   m5 : port 443/tcp (HTTP) as destination, are jumped to DROP chain (dropped packets)
    #   m6 : port 443/udp (HTTP) as destination, are jumped to DROP chain (dropped packets)
    #   m7 : PYCAPTIVE chain -> move on to NAT table with a mark set (Kernel tag)
    #   m8 : INTERNET chain -> move on to NAT table and to Internet (see m_comment_* below)
    #
    m_head="*mangle\n"
    m_counter_pre=":PREROUTING ACCEPT [0:0]\n"
    m_counter_input=":INPUT ACCEPT [0:0]\n"
    m_counter_forward="FORWARD ACCEPT [0:0]\n"
    m_counter_output=":OUTPUT ACCEPT [0:0]\n"
    m_counter_post=":POSTROUTING ACCEPT [0:0]\n"
    m_comment_1="# Internet access is provided after successful PyCaptive login"
    m_comment_2="# which add rules on top of *mangle table, above these chains\n"
    m1="-N INTERNET\n"
    m2="-N PYCAPTIVE\n"

    m3="-A PREROUTING -i {0} -p tcp -m tcp --dport {1} -j PYCAPTIVE\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["HTTP"])

    m4="-A PREROUTING -i {0} -p tcp -m ucp --dport {1} -j PYCAPTIVE\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["HTTP"])

    m5="-A PREROUTING -i {0} -p tcp -m tcp --dport {1} -j DROP\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["HTTPS"])

    m6="-A PREROUTING -i {0} -p tcp -m udp --dport {1} -j DROP\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["HTTPS"])

    m7="-A PYCAPTIVE -j MARK --set-mark 1\n"
    m8="-A INTERNET -j ACCEPT\n"
    
    # Table [NAT]
    #
    #   Packet Flow:
    #
    #   n1 : 80/tcp (HTTP) as destination, to NGINX -> GUNICORN (PyCaptive)
    #   n2 : 80/udp (HTTP) as destination, to NGINX -> GUNICORN (PyCaptive)
    #   n3 : PyCaptive portal accesible after successful login (admin purposes)
    #   n4 : 80/tcp (HTTP) as destination -> Transparent Proxy (depends on TestingConfig mode)
    #   n5 : masquerades LAN IPs, presenting WAN IP address for the Internet
    #   n6 : external web servers (Internet) -> redirected to Proxy (depends on TestingConfig mode)
    #
    n_head="*nat\n"
    n_counter_pre=":PREROUTING ACCEPT [0:0]\n"
    n_counter_input=":INPUT ACCEPT [0:0]\n"
    n_counter_ouput=":OUTPUT ACCEPT [0:0]\n"
    n_counter_post=":POSTROUTING ACCEPT [0:0]\n"

    n1="-A PREROUTING -i {0} -p tcp -m tcp -m mark --mark 1 -j DNAT --to-destination {1}:{2}\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["LAN_IP"],
                        app.config['CONFIG_GENERATOR_DICT']["NGINX_REDIR_GUNICORN"])

    n2="-A PREROUTING -i {0} -p udp -m udp -m mark --mark 1 -j DNAT --to-destination {1}:{2}\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["LAN_IP"],
                        app.config['CONFIG_GENERATOR_DICT']["NGINX_REDIR_GUNICORN"])

    n3="-A PREROUTING -i {0} -s {1} -p tcp -d {2} --dport {3} -j DNAT --to-destination {4}:{5}\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["LAN_NETWORK"],
                        app.config['CONFIG_GENERATOR_DICT']["LAN_IP"],
                        app.config['CONFIG_GENERATOR_DICT']["HTTP"],
                        app.config['CONFIG_GENERATOR_DICT']["LAN_IP"],
                        app.config['CONFIG_GENERATOR_DICT']["NGINX_REDIR_GUNICORN"])

    n4="-A PREROUTING -i {0} -s {1} -p tcp --dport {2} -j DNAT --to-destination {3}:{4}\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["LAN_NETWORK"],
                        app.config['CONFIG_GENERATOR_DICT']["HTTP"],
                        app.config['CONFIG_GENERATOR_DICT']["LAN_IP"],
                        app.config['CONFIG_GENERATOR_DICT']["PROXY"])

    n5="-A POSTROUTING -o {0} -j MASQUERADE\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["WAN"])

    n6="-A PREROUTING -i {0} -p tcp --sport {1} -j REDIRECT --to-port {2}\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["WAN"],
                        app.config['CONFIG_GENERATOR_DICT']["HTTP"],
                        app.config['CONFIG_GENERATOR_DICT']["PROXY"])

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
    f_head="*filter\n"
    f_counter_input=":INPUT ACCEPT [0:0]\n"
    f_counter_accept=":FORWARD ACCEPT [0:0]\n"
    f_counter_output=":OUTPUT ACCEPT [0:0]\n"
    f1="-A INPUT -p icmp -m conntrack --ctstate NEW,ESTABLISHED,RELATED --icmp-type 8 -j ACCEPT\n"
    f2="-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT\n"
    f3="-A INPUT -i lo -j ACCEPT\n"

    f4="-A INPUT -i {0} -p tcp --dport {1} -j ACCEPT\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["SSH"])

    f5="-A INPUT -i {0} -p udp --dport {1} -j ACCEPT\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["DNS"])

    f6="-A INPUT -i {0} -p tcp --dport {1} -j ACCEPT\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["DNS"])

    f7="-A INPUT -i {0} -p udp --dport {1} --sport {2} -j ACCEPT\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["DHCP_SERVER"],
                        app.config['CONFIG_GENERATOR_DICT']["DHCP_CLIENT"])

    f8="-A INPUT -i {0} -p udp --dport {1} --sport {2} -j ACCEPT\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["DHCP_CLIENT"],
                        app.config['CONFIG_GENERATOR_DICT']["DHCP_SERVER"])

    f9="-A INPUT -i {0} -p udp --dport {1} -j ACCEPT\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["DNS_RNDC"])

    f10="-A INPUT -i {0} -p tcp --dport {1} -j ACCEPT\n".format(
                        app.config['CONFIG_GENERATOR_DICT']["LAN"],
                        app.config['CONFIG_GENERATOR_DICT']["DNS_RNDC"])

    f11="-A INPUT -j REJECT\n"
    f12="-A OUTPUT -j ACCEPT\n"

    with open(FILE, "w") as f:

        # table [MANGLE]
        f.write(m_head)
        f.write(m_counter_pre)
        f.write(m_counter_input)
        f.write(m_counter_forward)
        f.write(m_counter_output)
        f.write(m_counter_post)
        f.write(m_comment_1)
        f.write(m_comment_2)
        f.write(m1)
        f.write(m2)
        f.write(m3)
        f.write(m4)
        f.write(m5)
        f.write(m6)
        f.write(m7)
        f.write(m8)

        # table [NAT]
        f.write(n_head)
        f.write(n_counter_pre)
        f.write(n_counter_input)
        f.write(n_counter_ouput)
        f.write(n_counter_post)
        f.write(n1)
        f.write(n2)
        f.write(n3)
        if app.config['CONFIG_GENERATOR_DICT']["MOD"] == 2:
            f.write(n4)
        f.write(n5)
        if app.config['CONFIG_GENERATOR_DICT']["MOD"] == 2:
            f.write(n6)

        # table [FILTER]
        f.write(f_head)
        f.write(f_counter_input)
        f.write(f_counter_accept)
        f.write(f_counter_output)
        f.write(f1)
        f.write(f2)
        f.write(f3)
        f.write(f4)
        f.write(f5)
        f.write(f6)
        f.write(f7)
        f.write(f8)
        f.write(f9)
        f.write(f10)
        f.write(f11)
        f.write(f12)


def nginx():

    FILE="deploy/nginx/pycaptive"

    print("- NGINX: ", FILE)

    ngx1="server {\n\n"
    ngx2="  listen {0}:{1};\n".format(
                app.config['CONFIG_GENERATOR_DICT']["LAN_IP"],
                app.config['CONFIG_GENERATOR_DICT']["NGINX_REDIR_GUNICORN"])

    ngx3="  server_name ~^(www\.)?(?<domain>.+)$;\n"
    ngx4="  return 301 $scheme://{0}:{1}/login;\n\n".format(
                app.config['CONFIG_GENERATOR_DICT']["LAN_IP"],
                app.config['CONFIG_GENERATOR_DICT']["NGINX_GUNICORN"])
    ngx5="  access_log /var/log/nginx/redirect_PyCaptive.access.log;\n"
    ngx6="  error_log /var/log/nginx/redirect_PyCaptive.error.log;\n\n}\n\n"

    ngx7="server {\n\n"
    ngx8="  listen {0}:{1};\n\n".format(
                app.config['CONFIG_GENERATOR_DICT']["LAN_IP"],
                app.config['CONFIG_GENERATOR_DICT']["NGINX_GUNICORN"])
    ngx9="  location / {\n"
    ngx10="     include proxy_params;\n"
    ngx11="     proxy_pass http://unix:/opt/PyCaptive/wsgi.sock;\n"
    ngx12="  }\n\n"
    ngx13="  access_log /var/log/nginx/PyCaptive.access.log;\n"
    ngx14="  error_log /var/log/nginx/PyCaptive.error.log;\n\n}"

    with open(FILE, "w") as f:
        f.write(ngx1)
        f.write(ngx2)
        f.write(ngx3)
        f.write(ngx4)
        f.write(ngx5)
        f.write(ngx6)
        f.write(ngx7)
        f.write(ngx8)
        f.write(ngx9)
        f.write(ngx10)
        f.write(ngx11)
        f.write(ngx12)
        f.write(ngx13)
        f.write(ngx14)


def sudoers():

    FILE="deploy/sudoers.d/pycaptive"

    print("- SUDOERS: ", FILE)

    sdr1="pycaptive ALL=(root:root) NOPASSWD:/sbin/iptables\n"
    sdr2="pycaptive ALL=(root:root) NOPASSWD:/usr/sbin/conntrack\n"

    with open(FILE, "w") as f:
        f.write(sdr1)
        f.write(sdr2)


def supervisor():

    FILE="deploy/supervisor/pycaptive.conf"

    print("- SUPERVISOR: ", FILE)

    s1="[program:pycaptive]\n"
    s2="command=gunicorn -n gnc_master -u gunicorn -g gunicorn -b unix:/opt/PyCaptive/wsgi.sock -w 2 --pythonpath /opt/PyCaptive app:app\n"
    s3="process_name=pycaptive\n"
    s4="autostart=true\n"
    s5="autorestart=true\n"
    s6="stderr_logfile=/var/log/supervisor/pycaptive.supervisor.err.log\n"
    s7="stdout_logfile=/var/log/supervisor/pycaptive.supervisor.out.log\n"

    with open(FILE, "w") as f:
        f.write(s1)
        f.write(s2)
        f.write(s3)
        f.write(s4)
        f.write(s5)
        f.write(s6)
        f.write(s7)

def logrotate():

    FILE="deploy/logrotate/pycaptive"

    print("- LOGROTATE: ", FILE)

    log1="/var/log/pycaptive/*.log {\n"
    log2="        monthly\n"
    log3="        missingok\n"
    log4="        rotate 12\n"
    log5="        compress\n"
    log6="        delaycompress\n"
    log7="        notifempty\n"
    log8="        postrotate\n"
    log9="                supervisorctl reload\n"
    log10="        endscript\n"
    log11="}"

    with open(FILE, "w") as f:
        f.write(log1)
        f.write(log2)
        f.write(log3)
        f.write(log4)
        f.write(log5)
        f.write(log6)
        f.write(log7)
        f.write(log8)
        f.write(log9)
        f.write(log10)
        f.write(log11)


print("Building configuration files: ")
iptables()
nginx()
sudoers()
supervisor()
logrotate()
