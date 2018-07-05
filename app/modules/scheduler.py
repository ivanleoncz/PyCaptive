#!/usr/bin/python3
""" APScheculer for monitoring expired sessions.  

According to the time defined at the end of the module,
the "expirer()" function runs, performing a query on the database,
which delivers a list of expired sessions (IPs).

This list of sessions, is passed to iptables module, specifically to
"del_rules()" method, which eliminates the IPTABLES rules and all
the connections related with the IP address on conntrack table.

INFO: APScheduler is started when the module is imported.
"""

from app import log
from app.modules import mongodb
from app.modules import iptables
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def expirer():
    """ Cleaning expired sessions """
    ts = datetime.now()
    log.error('[%s] %s %s %s',
        ts, "scheduler", "expirer", "RUNNING")
    db = mongodb.Connector()
    sessions = db.expire_sessions() # querying expired sessions
    if type(sessions) == list:
        if len(sessions) > 0:
            fw = iptables.Worker()
            counter = fw.del_rules(sessions) # deleting rules
            if type(counter) != int:
                log.error('[%s] %s %s %s',
                  ts, "scheduler", "expirer", "FAIL_IPTABLES")
    else:
        log.error('[%s] %s %s %s',
          ts, "scheduler", "expirer", "FAIL_MONGODB")


sched = BackgroundScheduler(daemon=True)
sched.add_job(expirer, 'interval', seconds=60)
sched.start()


