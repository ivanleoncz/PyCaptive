from app.pycaptive_settings import conf_iptables as conf


def iptables():

    FILE="rules.v4"


    # MANGLE ------------------------------------------------------------------------------------------------------------------
    mangle_head="*mangle\n"
    m_counter_pre=":PREROUTING ACCEPT [0:0]\n"
    m_counter_input=":INPUT ACCEPT [0:0]\n"
    m_counter_forward="FORWARD ACCEPT [0:0]\n"
    m_counter_output=":OUTPUT ACCEPT [0:0]\n"
    m_counter_post=":POSTROUTING ACCEPT [0:0]\n"
    m_chain_internet="-N INTERNET\n"
    m_chain_pycaptive="-N PYCAPTIVE\n"
    m_http_tcp="-A PREROUTING -i {0} -p tcp -m tcp --dport {1} -j PYCAPTIVE\n".format(conf["LAN"], conf["HTTP"])
    m_http_udp="-A PREROUTING -i {0} -p tcp -m ucp --dport {1} -j PYCAPTIVE\n".format(conf["LAN"], conf["HTTP"])
    m_https_tcp="-A PREROUTING -i {0} -p tcp -m tcp --dport {1} -j DROP\n".format(conf["LAN"], conf["HTTPS"])
    m_https_udp="-A PREROUTING -i {0} -p tcp -m udp --dport {1} -j DROP\n".format(conf["LAN"], conf["HTTPS"])
    m_jump_pycaptive="-A PYCAPTIVE -j MARK --set-mark 1\n"
    m_accept_internet="-A INTERNET -j ACCEPT\n"

    
    # NAT ---------------------------------------------------------------------------------------------------------------------
    nat_head="*nat\n"
    n_counter_pre=":PREROUTING ACCEPT [0:0]\n"
    n_counter_input=":INPUT ACCEPT [0:0]\n"
    n_counter_ouput=":OUTPUT ACCEPT [0:0]\n"
    n_counter_post=":POSTROUTING ACCEPT [0:0]\n"
    n_nginx_tcp="-A PREROUTING -i {0} -p tcp -m tcp -m mark --mark 1 -j DNAT --to-destination {1}:{2}\n".format(
                                                            conf["LAN"], conf["LAN_IP"], conf["NGINX_PYCAPTIVE"])
    n_nginx_udp="-A PREROUTING -i {0} -p udp -m tcp -m mark --mark 1 -j DNAT --to-destination {1}:{2}\n".format(
                                                            conf["LAN"], conf["LAN_IP"], conf["NGINX_PYCAPTIVE"])
    n_nginx_pycaptive_portal="-A PREROUTING -i {0} -s {1} -p tcp -d {2} --dport {3} -j DNAT --to-destination {4}:{5}\n".format(
                        conf["LAN"], conf["LAN_NETWORK"], conf["LAN_IP"], conf["HTTP"], conf["LAN_IP"], conf["NGINX_PYCAPTIVE"])
    n_transparent_proxy="-A PREROUTING -i {0} -s {1} -p tcp --dport {2} -j DNAT --to-destination {3}:{4}\n".format(
                                      conf["LAN"], conf["LAN_NETWORK"], conf["HTTP"], conf["LAN_IP"], conf["PROXY"])
    n_route_masquerade="-A POSTROUTING -o {0} -j MASQUERADE\n".format(conf["WAN"])
    n_transparent_proxy_force_http="-A PREROUTING -i {0} -p tcp --sport {1} -j REDIRECT --to-port {2}\n".format(
                                                                        conf["LAN"], conf["HTTP"], conf["PROXY"])


    # FILTER ------------------------------------------------------------------------------------------------------------------
    filter_head="*filter\n"
    f_counter_input=":INPUT ACCEPT [0:0]\n"
    f_counter_accept=":FORWARD ACCEPT [0:0]\n"
    f_counter_output=":OUTPUT ACCEPT [0:0]\n"
    f_icmp="-A INPUT -p icmp -m conntrack --ctstate NEW,ESTABLISHED,RELATED --icmp-type 8 -j ACCEPT\n"
    f_established="-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT\n"
    f_loopback="-A INPUT -i lo -j ACCEPT\n"
    f_ssh="-A INPUT -i {0} -p tcp --dport {1} -j ACCEPT\n".format(conf["LAN"], conf["SSH"])
    f_dns_udp="-A INPUT -i {0} -p udp --dport {1} -j ACCEPT\n".format(conf["LAN"], conf["DNS"])
    f_dns_tcp="-A INPUT -i {0} -p tcp --dport {1} -j ACCEPT\n".format(conf["LAN"], conf["DNS"])
    f_dhcp_client="-A INPUT -i {0} -p udp --dport {1} --sport {2} -j ACCEPT\n".format(conf["LAN"], conf["DHCP_SERVER"], conf["DHCP_CLIENT"])
    f_dhcp_server="-A INPUT -i {0} -p udp --dport {1} --sport {2} -j ACCEPT\n".format(conf["LAN"], conf["DHCP_CLIENT"], conf["DHCP_SERVER"])
    f_bind_rndc_udp="-A INPUT -i {0} -p udp --dport {1} -j ACCEPT\n".format(conf["LAN"], conf["DNS_RNDC"])
    f_bind_rndc_tcp="-A INPUT -i {0} -p tcp --dport {1} -j ACCEPT\n".format(conf["LAN"], conf["DNS_RNDC"])
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
        f.write(m_chain_internet)
        f.write(m_chain_pycaptive)
        f.write(m_http_tcp)
        f.write(m_http_udp)
        f.write(m_https_tcp)
        f.write(m_https_udp)
        f.write(m_jump_pycaptive)
        f.write(m_accept_internet)
        # nat
        f.write(nat_head)
        f.write(n_counter_pre)
        f.write(n_counter_input)
        f.write(n_counter_ouput)
        f.write(n_counter_post)
        f.write(n_nginx_tcp)
        f.write(n_nginx_udp)
        f.write(n_nginx_pycaptive_portal)
        if conf["MOD"] == 2:
            f.write(n_transparent_proxy)
        f.write(n_route_masquerade)
        if conf["MOD"] == 2:
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

iptables()
