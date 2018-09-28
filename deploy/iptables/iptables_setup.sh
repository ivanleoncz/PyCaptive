#!/bin/bash

. iptables_functions

# MOD 1: ROUTER
# MOD 2: ROUTER + TRANSPARENT PROXY
MOD=1
IPTABLES="/sbin/iptables"
LAN_NETWORK="192.168.0.0/24"
SRV_IPADDR="192.168.0.1"
LAN="eth2"
WAN="eth1"
HTTP="80"
HTTPS="443"
SSH="22"
DNS="53"
DHCP_SERVER="67"
DHCP_CLIENT="68"
DNS_RNDC="953"
PROXY="3128"
NGINX_PYCAPTIVE="14091"

echo "----------------------"
echo " Configuration Review "
echo "----------------------"
echo
echo "Server IP Address: $SRV_IPADDR"
echo "LAN Network: $LAN_NETWORK"
echo "LAN Interface: $LAN"
echo "WAN Interface: $WAN"
echo "HTTP: $HTTP"
echo "HTTPS: $HTTPS"
echo "DNS: $DNS"
echo "DNS Management: $DNS_RNDC"
echo "DHCP Server: $DHCP_SERVER"
echo "DHCP Client: $DHCP_CLIENT"
echo "PYCAPTIVE: $NGINX_PYCAPTIVE"
if [ $MOD -eq 2 ]; then
    echo "PROXY: $PROXY"
    echo "Configuration Mode: ROUTER + TRANSPARENT PROXY"
elif [ $MOD -eq 1 ]; then
    echo "Configuration Mode: ROUTER"
else
    echo "Configuraion Mode: NOT RECOGNIZED."
    exit 1
fi

echo -e "\n----------------------------------"
read -p "Proceed with configuration (y/n)? " OPT
if [[ $OPT == "y" ]] ; then
    echo "Processing..."
    iptables_setup
elif [[ $OPT == "n" ]]; then
    echo "Aborted!"
    exit 1
else
    echo "Not recognized!"
    exit 1
fi



function iptables_setup {

    # clearing counters, rules and custom chains
    $IPTABLES -Z
    $IPTABLES -F
    $IPTABLES -X
    $IPTABLES -t mangle -F
    $IPTABLES -t mangle -X
    $IPTABLES -t nat -F
    $IPTABLES -t nat -X
    $IPTABLES -t filter -F
    $IPTABLES -t filter -X
    
    # *mangle setup
    $IPTABLES -t mangle -N INTERNET
    $IPTABLES -t mangle -N PYCAPTIVE
    $IPTABLES -t mangle -A PREROUTING -i $LAN -p tcp -m tcp --dport $HTTP -j PYCAPTIVE
    $IPTABLES -t mangle -A PREROUTING -i $LAN -p udp -m udp --dport $HTTP -j PYCAPTIVE
    $IPTABLES -t mangle -A PREROUTING -i $LAN -p tcp -m tcp --dport $HTTPS -j DROP
    $IPTABLES -t mangle -A PREROUTING -i $LAN -p udp -m udp --dport $HTTPS -j DROP
    $IPTABLES -t mangle -A PYCAPTIVE -j MARK --set-mark 1
    $IPTABLES -t mangle -A INTERNET -j ACCEPT

    # *nat setup
    $IPTABLES -t nat -A PREROUTING -i $LAN -p tcp -m tcp -m mark --mark 1 -j DNAT --to-destination $SRV_IPADDR:$NGINX_PYCAPTIVE
    $IPTABLES -t nat -A PREROUTING -i $LAN -p udp -m udp -m mark --mark 1 -j DNAT --to-destination $SRV_IPADDR:$NGINX_PYCAPTIVE
    $IPTABLES -t nat -A PREROUTING -i $LAN -s $LAN_NETWORK -p tcp -d $SRV_IPADDR --dport $HTTP -j DNAT --to-destination $SRV_IPADDR:$NGINX_PYCAPTIVE
    
    if [ $MOD -eq 2 ] ; then
        $IPTABLES -t nat -A PREROUTING -i $LAN -s $LAN_NETWORK -p tcp --dport $HTTP -j DNAT --to-destination $SRV_IPADDR:$PROXY
    fi
    
    $IPTABLES -t nat -A POSTROUTING -o $WAN -j MASQUERADE

    if [ $MOD -eq 2 ] ; then
        $IPTABLES -t nat -A PREROUTING -i eth1 -p tcp --sport $HTTP -j REDIRECT --to-port $PROXY
    fi

    # *filter setup
    $IPTABLES -t filter -A INPUT -p icmp -m conntrack --ctstate NEW,ESTABLISHED,RELATED --icmp-type 8 -j ACCEPT
    $IPTABLES -t filter -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
    $IPTABLES -t filter -A INPUT -i lo -j ACCEPT
    $IPTABLES -t filter -A INPUT -i $LAN -p tcp --dport $SSH -j ACCEPT
    $IPTABLES -t filter -A INPUT -i $LAN -p udp --dport $DNS -j ACCEPT
    $IPTABLES -t filter -A INPUT -i $LAN -p tcp --dport $DNS -j ACCEPT
    $IPTABLES -t filter -A INPUT -i $LAN -p udp --dport $DHCP_SERVER --sport $DHCP_CLIENT -j ACCEPT                         
    $IPTABLES -t filter -A INPUT -i $LAN -p udp --dport $DHCP_CLIENT --sport $DHCP_SERVER -j ACCEPT 
    $IPTABLES -t filter -A INPUT -i $LAN -p udp --dport $DNS_RNDC -j ACCEPT
    $IPTABLES -t filter -A INPUT -i $LAN -p tcp --dport $DNS_RNDC -j ACCEPT
    $IPTABLES -t filter -A INPUT -j REJECT
    $IPTABLES -t filter -A OUTPUT -j ACCEPT
}
