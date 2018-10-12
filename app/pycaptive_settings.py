# PyCaptive Standalone Mode
HOST="0.0.0.0"
PORT=14090

# iptables module
IPTABLES="/sbin/iptables"
TABLE="mangle"
CHAIN="PREROUTING"
LAN="eth2"
JUMP="INTERNET"
