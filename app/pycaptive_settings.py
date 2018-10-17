# PyCaptive Settings
#
# Configurations defined here are restricted to PyCaptive operation.
#
# For Flask Environment Variables, see flask_settings.py.
#
# INFO: some variables are self-explanatory.

# <PyCaptive Standalone Mode>

HOST="0.0.0.0"
PORT=14090

# <Per Module Configuration>

# [IPTABLES]
#
# Unless you're performing a very specific customization, the only variable
# that should be changed here is the LAN variable, according with the setup
# of your network server.
#
IPTABLES="/sbin/iptables"
TABLE="mangle"
CHAIN="PREROUTING"
LAN="eth2"
JUMP="INTERNET"

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
# SESSION_DURATION defines for how long (hours) a UserName/IpAddress
# will have Internet access. PyCaptive will be verifying from time
# to time (SCHEDULER module) on its MongoDB database, the sessions which
# have reached the SESSION_DURATION time, expiring these sessions, one by one.
#
DB_USER="mongo"
DB_PASS="mongo"
DB_ADDR="127.0.0.1:27017"
DB_URI="mongodb://{0}:{1}@{2}".format(DB_USER, DB_PASS, DB_ADDR)
SESSION_DURATION=12

# [SCHEDULER]
#
# Defines the time interval (seconds )that PyCaptive will consider for
# verifying expired sessions on its MongoDB database.
#
# Unless you need something very specific, leave this variable as it is.
#
TIME_INTERVAL=60
