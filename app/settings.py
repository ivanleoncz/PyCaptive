#
#   PyCaptive Global Settings
#
#   ----------------------------------------------------------------------
#
#   Configurations defined here are restricted to PyCaptive configuration.
#
#   For Flask Environment Variables, see flask_settings.py.
DEBUG=False

# If DEBUG=True, define a fixed SECRET_KEY, in order to avoid
# possible conflicts, for this option launches two instances
# of a Flask app and both will have different secrets.
#
# Like this:
#
# SECRET_KEY=b'bN_(/_3#@-,lK2cpO-\,c3.?'
SECRET_KEY='write a unique secret key'

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
LAN_IP='127.0.0.1'  # get_nic_ip(NETWORK_LAN_NIC)
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(message)s - %(name)s:%(lineno)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'INFO',
            'filters': [],
        },
    },
}

##########################################################################
#
#   Configuration Dictionaries
#
##########################################################################

CONFIG_GENERATOR_DICT = {
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
    "NGINX_GUNICORN": PORT_NGINX_GUNICORN
}

CHECKSYS_DICT = {
    "IPTABLES":IPT_IPTABLES,
    "CONNTRACK":IPT_CONNTRACK,
    "NGINX_REDIR":(LAN_IP, PORT_NGINX_REDIR_GUNICORN),
    "NGINX_GUNICORN":(LAN_IP, PORT_NGINX_GUNICORN),
    "MONGODB":(DB_ADDR, DB_PORT),
}

IPTABLES_DICT = {
    "IPTABLES":IPT_IPTABLES,
    "CONNTRACK":IPT_CONNTRACK,
    "TABLE":IPT_TABLE,
    "CHAIN":IPT_CHAIN,
    "LAN":LAN_NIC,
    "JUMP":IPT_JUMP,
    "COMMENT":IPT_COMMENT
}

MONGODB_DICT = {
    "URI":DB_URI,
    "SESSION_DURATION":DB_SESSION_DURATION
}

SCHEDULER_DICT = {
    "INTERVAL":SCHEDULER_INTERVAL
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
    IPTABLES_DICT["LAN"] = "lo"
    IPTABLES_DICT["JUMP"] = "ACCEPT"
    IPTABLES_DICT["COMMENT"] = "Added via PyCaptive [Test Mode]"
    # logger
    # mongodb
    MONGODB_DICT["SESSION_DURATION"] = 300
    # scheduler
    SCHEDULER_DICT["INTERVAL"] = 60
