#
#   PyCaptive Global Settings
#
#   ----------------------------------------------------------------------
#
#   Configurations defined here are restricted to PyCaptive operation,
#   for two contexts:
#
#       - PyCaptive Modules
#       - Configuration Generator (config_generator.py)
#
#   For Flask Environment Variables, see flask_settings.py.
#


# [FUNCTIONS]
#
# Designed for obtaining specific data on some variables.
#
def get_nic_ip(nic):
    """ Get IP address from a NIC."""
    import subprocess as sp
    result = sp.check_output(["ip", "addr", "show", nic])
    result = result.decode().split()
    ipaddr = result[result.index('inet') + 1].split('/')[0]
    return ipaddr


# [GLOBAL]
#
# Variables defined here, have impact on both contexts.
#
# - defines the LAN NIC (network interface card) where PyCaptive will be running on
NIC="eth2"


# [IPTABLES]
#
# Unless you're performing a very specific customization, the only variable
# that should be changed here is the LAN variable, according with the setup
# of your network server, and COMMENT, which is added on each IPTABLES/Netfilter
# rule for granting Internet Access to an specific IP address.
#
# Notice: some variables, are algo used by config_generator.py
#
IPTABLES="/sbin/iptables"
CONNTRACK="/usr/sbin/conntrack"
TABLE="mangle"
CHAIN="PREROUTING"
LAN=NIC
JUMP="INTERNET"
COMMENT="Added via PyCaptive"


# [LOGGER]
#
# If LOG_ROTATE=True, logging.handlers.TimedRotatingFileHandler will be used
# for log rotation, instead of the default logrotate tool from the OS.
#
# For more info: https://docs.python.org/3.5/library/logging.handlers.html
#
# Example: rotates every Sunday (weekly), keeping logs for a whole year.
#
LOG_FILE="/var/log/pycaptive/pycaptive.log"
LOG_ROTATE=False
LOG_ROTATE_WHEN='W6'
LOG_ROTATE_COUNT=52


# [MONGODB]
#
# SESSION_DURATION defines for how long (seconds) a UserName/IpAddress
# will have Internet access. PyCaptive will be verifying from time
# to time (SCHEDULER module) on its MongoDB database, the sessions which
# have reached the SESSION_DURATION time, expiring these sessions, one by one.
#
DB_USER="mongo"
DB_PASS="mongo"
DB_ADDR="127.0.0.1"
DB_PORT="27017"
DB_URI="mongodb://{0}:{1}@{2}:{3}".format(DB_USER, DB_PASS, DB_ADDR, DB_PORT)
SESSION_DURATION=43200 # 12 hours


# [SCHEDULER]
#
# Defines the time interval (seconds) that PyCaptive will consider for
# verifying expired sessions on its MongoDB database.
#
# Unless you need something very specific, leave this variable as it is.
#
SCHEDULER_INTERVAL=60


# [CONFIG GENERATOR]
#
# Variables defined here are reserved to "config_generator.py" and its routines
# for generating configuration files (see deploy directory).
#
# - MOD 1 : iptables (ROUTER + FIREWALL)
# - MOD 2 : iptables (ROUTER + FIREWALL + TRANSPARENT PROXY)
#
conf_generator = {
        "MOD":1,
        "LAN":NIC,
        "LAN_IP":get_nic_ip(NIC),
        "WAN":"eth1",
        "LAN_NETWORK":"192.168.0.0/24",
        "HTTP":"80",
        "HTTPS":"443",
        "SSH":"22",
        "DNS":"53",
        "DNS_RNDC":"953",
        "DHCP_SERVER":"67",
        "DHCP_CLIENT":"68",
        "PROXY":"3128",
        "NGINX_REDIR_GUNICORN":"14901",
        "GUNICORN":"14900"
}


# [TEST MODE]
#
# When TEST flag is True, some variables from this file are redefined, in order
# to configure PyCaptive in its Test Mode (which does not include NGINX and
# GUNIRCORN for its operation).
#
# The loopback interface (lo/127.0.0.1) is used, in order to avoid interactions
# with the interfaces which are being used by the host in its normal network
# traffic, creating inoffensive rules on this context, in order to simulate
# PyCaptive's normal flow, regarding Authorizing and Revoking Internet access
# for an specific IP address:
#
# Authorizing: login -> add session -> add rule
# Revoking: scheduler -> check/delete session -> delete rule -> delete connections
#
TEST=False

if TEST is True:
    # [IPTABLES]
    LAN="lo"
    JUMP="ACCEPT"
    COMMENT="Added via PyCaptive [Test Mode]"
    # [LOGGER]
    LOG_FILE="/tmp/pycaptive_test_mode.log"
    # [MONGODB]
    SESSION_DURATION=300 # 5 minutes
    # [SCHEDULER]
    SCHEDULER_INTERVAL=60 # 1 minute
