#!/usr/bin/env python3

""" Scheduler for Login Sessions.  """

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from app import log
from app.modules import mongodb
from app.modules import iptables

def ses(): # Session Expiration Scheduler
    """ Verifies and expires sessions. """
    db = mongodb.Connector()
    sessions = mdbc.expire_sessions()
    if type(sessions) == list and len(sessions) > 0:
        log.error('%s %s %s %s', datetime.now(), "SCHEDULER", "EVENT:[Expired Sessions]", sessions)
        fw = iptables.Worker()
        counter = fw.test_del_rule(sessions)
        if type(counter) == int and counter > 0:
            log.error('%s %s %s %s', datetime.now(), "SCHEDULER",  "EVENT:[Removed Rules]", counter)
        else:
            log.error('%s %s %s %s', datetime.now(), "SCHEDULER", "EVENT:[Fail To Remove Rules]", counter)
    else:
        log.error('%s %s %s %s', datetime.now(), "SCHEDULER",  "EVENT:[No Session To Expire]", sessions)

sched = BackgroundScheduler(daemon=True)
sched.add_job(ses,'interval',seconds=60)
sched.start()
