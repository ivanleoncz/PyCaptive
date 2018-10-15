# PyCaptive Settings
#
# Configurations defined here are restricted to PyCaptive setup.
#
# For Flask Environment Variables, see flask_settings.py.

# PyCaptive Standalone Mode
HOST="0.0.0.0"
PORT=14090

# iptables module
IPTABLES="/sbin/iptables"
TABLE="mangle"
CHAIN="PREROUTING"
LAN="eth2"
JUMP="INTERNET"
