""" APScheculer for monitoring expired sessions.  

Started when the module is imported, periodically performing
a sweep on MongoDB (see pycaptive_settings.py:TIME_INTERVAL),
searching for expired sessions (IPs).

The result is passed to iptables module, which eliminates
the rules associated with the IP addresses which are returned
via APScheduler.
"""

from apscheduler.schedulers.background import BackgroundScheduler

from app import log, SCHEDULER_INTERVAL
from app.modules import mongodb
from app.modules import iptables

__author__ = "@ivanleoncz"


def expirer():
    """ Searching/cleaning expired sessions """

    db = mongodb.Connector()
    # querying expired sessions
    sessions = db.expire_sessions()
    if type(sessions) == list:
        if len(sessions) > 0:
            fw = iptables.Worker()
            # deleting rules
            counter = fw.del_rules(sessions)
            if type(counter) == int:
                log.info('%s %s %s', "scheduler", "expirer", "OK")
            else:
                log.error('%s %s %s', "scheduler", "expirer", "FAIL_IPTABLES")

    else:
        log.error('%s %s %s', "scheduler", "expirer", "FAIL_MONGODB")


sched = BackgroundScheduler(daemon=True)
sched.add_job(expirer, 'interval', seconds=TIME_INTERVAL)
sched.start()
