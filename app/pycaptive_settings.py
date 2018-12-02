#
#   PyCaptive Global Settings
#
#   ----------------------------------------------------------------------
#
#   Configurations defined here are restricted to PyCaptive configuration.
#
#   For Flask Environment Variables, see flask_settings.py.


##########################################################################
#
#   Helper Functions
#
##########################################################################

def get_nic_ip(nic):
    """ Get IP address from a NIC."""
    import subprocess as sp
    result = sp.check_output(["ip", "addr", "show", nic])
    result = result.decode().split()
    ipaddr = result[result.index('inet') + 1].split('/')[0]
    return ipaddr


##########################################################################
#
#   Configuration Variables
#
#     Responsible for defining values for the Configuration Dictionaries.
#
##########################################################################

# activates custom configuration for Test Mode
TEST_MODE=False
# defines the network interface where PyCaptive will be working on
LAN_NIC="eth2"
LAN_IP=get_nic_ip(NETWORK_LAN_NIC)
LAN_NETWORK="192.168.0.0/24"
WAN_NIC="eth1"
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
# generation of a specific set or rules for iptables
#   1 (router + firewall)
#   2 (router + firewall + transparent proxy)
IPT_MODE=1
IPT_IPTABLES="/sbin/iptables"
IPT_CONNTRACK="/usr/sbin/conntrack"
IPT_TABLE="mangle"
IPT_CHAIN="PREROUTING"
IPT_JUMP="INTERNET"
IPT_COMMENT="Added via PyCaptive"
# defines if logrtation will be performed by OS binary (logrotate)
LOG_ROTATE_OS=True
# every sunday (weekly)
LOG_ROTATE_WHEN='W6'
# number of file retention (52 weeks == year)
LOG_ROTATE_COUNT=52
LOG_FILE="/var/log/pycaptive/pycaptive.log"
DB_USER="mongo"
DB_PASS="mongo"
DB_ADDR="127.0.0.1"
DB_PORT="27017"
DB_URI="mongodb://{0}:{1}@{2}:{3}".format(DB_USER, DB_PASS, DB_ADDR, DB_PORT)
# 12 hours of session (seconds)
DB_SESSION_DURATION=43200
# 1 minute of interval between checking/eliminating expired sessions (seconds)
SCHEDULER_INTERVAL=60


##########################################################################
#
#   Configuration Dictionaries
#
##########################################################################

config_generator_dict = {
        "MOD":IPT_MODE,
        "LAN":LAN_NIC,
        "LAN_IP":LAN_IP,
        "WAN":WAN_NIC,
        "LAN_NETWORK":LAN_NETWORK,
        "HTTP":PORT_HTTP,
        "HTTPS":PORT_HTTPS,
        "SSH":PORT_SSH,
        "DNS":PORT_DNS,
        "DNS_RNDC":PORT_DNS_RNDC,
        "DHCP_SERVER":PORT_DHCP_SERVER,
        "DHCP_CLIENT":PORT_DHCP_CLIENT,
        "PROXY":PORT_PROXY,
        "NGINX_REDIR_GUNICORN":PORT_NGINX_REDIR_GUNICORN,
        "NGINX_GUNICORN":PORT_NGINX_GUNICORN
}


checksys_dict = {
        "IPTABLES":IPT_IPTABLES,
        "CONNTRACK":IPT_CONNTRACK,
        "NGINX_REDIR":(LAN_IP, PORT_NGINX_REDIR_GUNICORN)
        "NGINX_GUNICORN":(LAN_IP, PORT_NGINX_GUNICORN)
        "MONGODB":(DB_ADDR, DB_PORT)
}


iptables_dict = {
    "IPTABLES":IPT_IPTABLES,
    "CONNTRACK":IPT_CONNTRACK,
    "TABLE":IPT_TABLE,
    "CHAIN":IPT_CHAIN,
    "LAN":LAN_NIC,
    "JUMP":IPT_JUMP,
    "COMMENT":IPT_COMMENT
}


mongodb_dict = {
    "URI":DB_URI,
    "SESSION_DURATION":DB_SESSION_DURATION
}


scheduler_dict = {
    "INTERVAL":SCHEDULER_INTERVAL
}


logger_dict = {
    "ROTATE_OS":LOG_ROTATE_OS,
    "ROTATE_WHEN":LOG_ROTATE_WHEN,
    "ROTATE_COUNT":LOG_ROTATE_COUNT,
    "FILE":LOG_FILE
}


# ----------------------------------------------------------------------------
#
#     If TEST_MODE flag is set as True, the Configuration Dictionaries
#     will be reprocessed, in order to adapt PyCaptive for this mode.
#
# ----------------------------------------------------------------------------

if TEST_MODE is True:
    # checksys
    del checksys["NGINX_REDIR"]
    del checksys["NGINX_GUNICORN"]
    # iptables
    iptables_dict["LAN"] = "lo"
    iptables_dict["JUMP"] = "ACCEPT"
    iptables_dict["COMMENT"] = "Added via PyCaptive [Test Mode]"
    # logger
    logger_dict["FILE"] = "/tmp/pycaptive_test_mode.log"
    # mongodb
    mongodb_dict["SESSION_DURATION"] = 300
    # scheduler
    scheduler_dict["INTERVAL"] = 60
