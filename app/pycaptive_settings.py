#
# PyCaptive Global Settings
#
# Configurations defined here are restricted to PyCaptive operation.
#
# For Flask Environment Variables, see flask_settings.py.
#

# [FUNCTIONS]
#
# Designed for obtaining specific data on some variables.
#
def get_nic_ip(nic):
    """ Get IP address from a NIC."""
    import subprocess as sp
    result = sp.check_output(["ip", "addr", "show", nic])
    result = result.split()
    ipaddr = result[result.index('inet') + 1].split('/')[0]
    return ipaddr


# [IPTABLES]
#
# Unless you're performing a very specific customization, the only variable
# that should be changed here is the LAN variable, according with the setup
# of your network server, and COMMENT, which is added on each IPTABLES/Netfilter
# rule for granting Internet Access to an specific IP address.
#
IPTABLES="/sbin/iptables"
TABLE="mangle"
CHAIN="PREROUTING"
LAN="eth2"
JUMP="INTERNET"
COMMENT="Added via PyCaptive"
CONNTRACK="/usr/sbin/conntrack"


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


# [SYSTEM]
#
# Variables defined here are reserved to "checksys" module and its routines.
#
WEBSERVER_IP=get_nic_ip(LAN)


# [TEST]
#
# Variables configured when TEST flag is activated, are just designed for
# PyCaptive in Test Mode and have no effect over the Operating System:
#
# Internet Access: login -> add session -> add rule
# Revoked Access:  scheduler -> check/del session -> del rule -> del connections
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
    SESSION_DURATION=300
    # [SCHEDULER]
    SCHEDULER_INTERVAL=30
