import os

class BaseConfig(object):
    """ Base Configuration """
    # Flask (default variables)
    DEBUG=False
    SECRET_KEY=os.urandom(24)

    # Network Setup
    # - interface where PyCaptive will be working on
    LAN_NIC="eth2"
    # - get_nic_ip(NETWORK_LAN_NIC)
    LAN_IP='127.0.0.1'
    LAN_NETWORK="192.168.0.0/24"
    WAN_NIC="eth1"

    # Firewall Rules
    PORT_HTTP="80"
    PORT_HTTPS="443"
    PORT_SSH="22"
    PORT_DNS="53"
    PORT_DNS_RNDC="953"
    PORT_DHCP_SERVER="67"
    PORT_DHCP_CLIENT="68"
    PORT_PROXY="3128"
    PORT_NGINX_REDIR_GUNICORN="14901"
    PORT_NGINX_GUNICORN="14900"
     # - Firewall Mode: 1 (normal) || 2 (with Transparent Proxy)
    IPT_MODE=1
    IPT_IPTABLES="/sbin/iptables"
    IPT_CONNTRACK="/usr/sbin/conntrack"
    IPT_TABLE="mangle"
    IPT_CHAIN="PREROUTING"
    IPT_JUMP="INTERNET"
    IPT_COMMENT="Added via PyCaptive"

    # Log Setup
    # - every sunday (weekly)
    LOG_ROTATE_WHEN='W6'
    # - number of file retention (52 weeks == year)
    LOG_ROTATE_COUNT=52
    LOG_FILE="/var/log/pycaptive/pycaptive.log"

    # Database Setup
    DB_USER="mongo"
    DB_PASS="mongo"
    DB_ADDR="127.0.0.1"
    DB_PORT="27017"
    DB_URI="mongodb://{0}:{1}@{2}:{3}".format(DB_USER, DB_PASS, DB_ADDR, DB_PORT)
    # - 12 hours of session (seconds)
    DB_SESSION_DURATION=43200

    # Scheduler Setup
    # - interval between verifying expired sessions (seconds)
    SCHEDULER_INTERVAL=60


class TestModeConfig(BaseConfig):
    """ Configuration for Test Mode """
    DEBUG=True
    SECRET_KEY="IAisoaijda83qadaishdzz/|,.>,-A987Q*(&SJ_0_(_)a(s@SW90/"
    TEST_MODE=True
    LAN_NIC="lo"
    IPT_JUMP="ACCEPT"
    IPT_COMMENT="Added via PyCaptive [Test Mode]"
    DB_SESSION_DURATION=300
    SCHEDULER_INTERVAL=60
