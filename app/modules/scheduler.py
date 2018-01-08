#!/usr/bin/env python3

""" Scheduler for Login Sessions.  """

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from app import log
from app.modules import mongodb
from app.modules import iptables

def expirer():
    """ Verifies and expires sessions. """
    log.error('[%s] %s %s %s %s', datetime.now(), "EVENT", "scheduler", "expirer" , "RUNNING")
    db = mongodb.Connector()
    sessions = db.expire_sessions()
    if type(sessions) == list:
        if len(sessions) > 0:
            fw = iptables.Worker()
            counter = fw.test_del_rule(sessions)
            if type(counter) != int:
                log.error('[%s] %s %s %s %s', datetime.now(), "EVENT", "scheduler", "expirer", "FAIL_IPTABLES")
    else:
        log.error('[%s] %s %s %s %s', datetime.now(), "EVENT", "scheduler", "expirer", "FAIL_MONGODB")


sched = BackgroundScheduler(daemon=True)
sched.add_job(expirer,'interval',seconds=60)
sched.start()


