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
NGINX_PYCAPTIVE="14901"

check_nf_conntrack=`lsmod | awk '{print $1}' | grep --color "nf_conntrack$"`
if [ -z `$check_nf_conntrack` ] ; then
    echo "INFO: No Netfilter's connection tracking module was found."
    echo "Aborted!"
    exit 1
fi

echo
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
echo "NGINX (redir. PyCaptive): $NGINX_PYCAPTIVE"

if [ $MOD -eq 1 ]; then
    echo -e "\nConfiguration Mode: ROUTER"
elif [ $MOD -eq 2 ]; then
    echo -e "\nConfiguration Mode: ROUTER + TRANSPARENT PROXY ($PROXY)"
else
    echo -e "\nConfiguration Mode: NOT RECOGNIZED."
    exit 1
fi

echo
echo "--------------------------------------------------------------"
echo " INFO: if proceeded, current Firewall setup will be backed up "
echo "--------------------------------------------------------------"
echo

read -p "Proceed (y/n) ? " OPT

if [[ $OPT == "y" ]] ; then
    backup
    cleaner
    mangle_setup
    nat_setup
    filter_setup
elif [[ $OPT == "n" ]] ; then
    echo "Aborted!"
    exit 1
else
    echo "Not recognized!"
    exit 1
fi
