from app.pycaptive_settings import v_iptables as v


def iptables():

    FILE="deploy/iptables/rules.v4"

    # Table [MANGLE]
    #
    # Concepts (rules):
    #
    #   m_chain_internet  : creates INTERNET chain
    #   m_chain_pycaptive : creates PYCAPTIVE chain
    #   m_http_tcp        : packets with port 80/tcp (HTTP) as destination, are jumped to PYCAPTIVE chain -> see "m_mark_pycaptive"
    #   m_http_udp        : packets with port 80/udp (HTTP) as destination, are jumped to PYCAPTIVE chain -> see "m_mark_pycaptive"
    #   m_https_tcp       : packets with port 443/tcp (HTTP) as destination, are jumped to DROP chain (dropped packets)
    #   m_https_udp       : packets with port 443/udp (HTTP) as destination, are jumped to DROP chain (dropped packets)
    #   m_mark_pycaptive  : packets received on PYCAPTIVE chain, will move on to NAT table, but with a mark/tag set (Kernel)
    #   m_accept_internet : packets received on INTERNET chain, will move on to NAT table, fully accepted -> see "m_comment"
    #
    mangle_head="*mangle\n"
    m_counter_pre=":PREROUTING ACCEPT [0:0]\n"
    m_counter_input=":INPUT ACCEPT [0:0]\n"
    m_counter_forward="FORWARD ACCEPT [0:0]\n"
    m_counter_output=":OUTPUT ACCEPT [0:0]\n"
    m_counter_post=":POSTROUTING ACCEPT [0:0]\n"
    m_comment="# access to clients is provided after successful login on PyCaptive, which adds rules on top of *mangle table, above these chains "
    m_chain_internet="-N INTERNET\n"
    m_chain_pycaptive="-N PYCAPTIVE\n"
    m_http_tcp="-A PREROUTING -i {0} -p tcp -m tcp --dport {1} -j PYCAPTIVE\n".format(v["LAN"], v["HTTP"])
    m_http_udp="-A PREROUTING -i {0} -p tcp -m ucp --dport {1} -j PYCAPTIVE\n".format(v["LAN"], v["HTTP"])
    m_https_tcp="-A PREROUTING -i {0} -p tcp -m tcp --dport {1} -j DROP\n".format(v["LAN"], v["HTTPS"])
    m_https_udp="-A PREROUTING -i {0} -p tcp -m udp --dport {1} -j DROP\n".format(v["LAN"], v["HTTPS"])
    m_mark_pycaptive="-A PYCAPTIVE -j MARK --set-mark 1\n"
    m_accept_internet="-A INTERNET -j ACCEPT\n"
    
    # Table [NAT]
    #
    # Concepts (rules):
    #
    #   n_ngx_tcp                      : routes marked tcp packets with port 80 as destination, to NGINX -> GUNICORN (PyCaptive)
    #   n_ngx_udp                      : routes marked udp packets with port 80 as destination, to NGINX -> GUNICORN (PyCaptive)
    #   n_ngx_pycaptive                : allows access to PyCaptive, without specifing port 14901. Ex.: browser -> "http://lan_ip_address" (default port/80)
    #   n_transparent_proxy            : routes packets with port 80 as destination, to Transparent Proxy (e.g., Squid3)
    #   n_route_masquerade             : hides the IP addresses of LAN when accessing servers through the Internet (WAN IP address is presented instead)
    #   n_transparent_proxy_force_http : ensures that packets coming from web servers (WAN/Internet) should be redirected to Proxy port
    #
    nat_head="*nat\n"
    n_counter_pre=":PREROUTING ACCEPT [0:0]\n"
    n_counter_input=":INPUT ACCEPT [0:0]\n"
    n_counter_ouput=":OUTPUT ACCEPT [0:0]\n"
    n_counter_post=":POSTROUTING ACCEPT [0:0]\n"
    n_ngx_tcp="-A PREROUTING -i {0} -p tcp -m tcp -m mark --mark 1 -j DNAT --to-destination {1}:{2}\n".format(v["LAN"], v["LAN_IP"], v["NGINX_PYCAPTIVE"])
    n_ngx_udp="-A PREROUTING -i {0} -p udp -m tcp -m mark --mark 1 -j DNAT --to-destination {1}:{2}\n".format(v["LAN"], v["LAN_IP"], v["NGINX_PYCAPTIVE"])
    n_ngx_pycaptive="-A PREROUTING -i {0} -s {1} -p tcp -d {2} --dport {3} -j DNAT --to-destination {4}:{5}\n".format(v["LAN"], v["LAN_NETWORK"], v["LAN_IP"], v["HTTP"],
                                                                                                                                v["LAN_IP"], v["NGINX_PYCAPTIVE"])

    n_transparent_proxy="-A PREROUTING -i {0} -s {1} -p tcp --dport {2} -j DNAT --to-destination {3}:{4}\n".format(v["LAN"], v["LAN_NETWORK"], v["HTTP"],
                                                                                                                                  v["LAN_IP"], v["PROXY"])

    n_route_masquerade="-A POSTROUTING -o {0} -j MASQUERADE\n".format(v["WAN"])
    n_transparent_proxy_force_http="-A PREROUTING -i {0} -p tcp --sport {1} -j REDIRECT --to-port {2}\n".format(v["WAN"], v["HTTP"], v["PROXY"])

    # table: [FILTER]
    #
    # Concepts (rules):
    #
    #   f_icmp          : allowing ICMP traffic (all interfaces)
    #   f_established   : allowing incomming traffic that was already established (all interfaces)
    #   f_loopback      : allowing localhost traffic
    #   f_ssh           : allowing incoming SSH traffic (LAN)
    #   f_dns_udp       : allowing incoming DNS/udp traffic (LAN)
    #   f_dns_tcp       : allowing incoming DNS/tcp traffic (LAN)
    #   f_dhcp_client   : allowing incoming DHCP/tcp client traffic (LAN)
    #   f_dhcp_server   : allowing incoming DHCP/tcp server traffic (LAN)
    #   f_bind_rndc_udp : allowing incoming DNS control via RNDC/udp traffic (LAN)
    #   f_bind_rndc_tcp : allowing incoming DNS control via RNDC/tcp traffic (LAN)
    #   f_input_block   : blocking all incoming connections not listed above (all interfaces)
    #   f_output_accept : accept all outcome traffic (all interfaces)
    #
    filter_head="*filter\n"
    f_counter_input=":INPUT ACCEPT [0:0]\n"
    f_counter_accept=":FORWARD ACCEPT [0:0]\n"
    f_counter_output=":OUTPUT ACCEPT [0:0]\n"
    f_icmp="-A INPUT -p icmp -m conntrack --ctstate NEW,ESTABLISHED,RELATED --icmp-type 8 -j ACCEPT\n"
    f_established="-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT\n"
    f_loopback="-A INPUT -i lo -j ACCEPT\n"
    f_ssh="-A INPUT -i {0} -p tcp --dport {1} -j ACCEPT\n".format(v["LAN"], v["SSH"])
    f_dns_udp="-A INPUT -i {0} -p udp --dport {1} -j ACCEPT\n".format(v["LAN"], v["DNS"])
    f_dns_tcp="-A INPUT -i {0} -p tcp --dport {1} -j ACCEPT\n".format(v["LAN"], v["DNS"])
    f_dhcp_client="-A INPUT -i {0} -p udp --dport {1} --sport {2} -j ACCEPT\n".format(v["LAN"], v["DHCP_SERVER"], v["DHCP_CLIENT"])
    f_dhcp_server="-A INPUT -i {0} -p udp --dport {1} --sport {2} -j ACCEPT\n".format(v["LAN"], v["DHCP_CLIENT"], v["DHCP_SERVER"])
    f_bind_rndc_udp="-A INPUT -i {0} -p udp --dport {1} -j ACCEPT\n".format(v["LAN"], v["DNS_RNDC"])
    f_bind_rndc_tcp="-A INPUT -i {0} -p tcp --dport {1} -j ACCEPT\n".format(v["LAN"], v["DNS_RNDC"])
    f_input_block="-A INPUT -j REJECT\n"
    f_output_accept="-A OUTPUT -j ACCEPT\n"

    with open(FILE, "w") as f:
        # mangle
        f.write(mangle_head)
        f.write(m_counter_pre)
        f.write(m_counter_input)
        f.write(m_counter_forward)
        f.write(m_counter_output)
        f.write(m_counter_post)
        f.write(m_comment)
        f.write(m_chain_internet)
        f.write(m_chain_pycaptive)
        f.write(m_http_tcp)
        f.write(m_http_udp)
        f.write(m_https_tcp)
        f.write(m_https_udp)
        f.write(m_mark_pycaptive)
        f.write(m_accept_internet)
        # nat
        f.write(nat_head)
        f.write(n_counter_pre)
        f.write(n_counter_input)
        f.write(n_counter_ouput)
        f.write(n_counter_post)
        f.write(n_ngx_tcp)
        f.write(n_ngx_udp)
        f.write(n_ngx_pycaptive)
        if v["MOD"] == 2:
            f.write(n_transparent_proxy)
        f.write(n_route_masquerade)
        if v["MOD"] == 2:
            f.write(n_transparent_proxy_force_http)
        # filter
        f.write(filter_head)
        f.write(f_counter_input)
        f.write(f_counter_accept)
        f.write(f_counter_output)
        f.write(f_icmp)
        f.write(f_established)
        f.write(f_loopback)
        f.write(f_ssh)
        f.write(f_dns_udp)
        f.write(f_dns_tcp)
        f.write(f_dhcp_client)
        f.write(f_dhcp_server)
        f.write(f_bind_rndc_udp)
        f.write(f_bind_rndc_tcp)
        f.write(f_input_block)
        f.write(f_output_accept)


def supervisor():

    FILE="deploy/supervisor/supervisor.conf"

    supervisor_head="[program:pycaptive]\n"
    command="gunicorn n gunicorn_master -u gunicorn -g gunicorn -b unix:/opt/PyCaptive/wsgi.sock -w 2 --pythonpath /opt/PyCaptive app:app\n"
    process_name="process_name=pycaptive\n"
    autostart="autostart=true\n"
    autorestart="autorestart=true\n"
    stderr_logfile="stderr_logfile=/var/log/supervisor/pycaptive.supervisor.err.log\n"
    stdout_logfile="stdout_logfile=/var/log/supervisor/pycaptive.supervisor.out.log\n"

    with open(FILE, "w") as f:
        f.write(supervisor_head)
        f.write(command)
        f.write(process_name)
        f.write(autostart)
        f.write(autorestart)
        f.write(stderr_logfile)
        f.write(stderr_logfile)

iptables()
supervisor()
