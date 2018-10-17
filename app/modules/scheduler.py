""" APScheculer for monitoring expired sessions.  

APScheduler is started when the module is imported
and it periodically performs (see INTERVAL_TIME)
a sweep on MongoDB, searching for expired sessions (IPs).

The result is passed to iptables module, which eliminates
the rules associated with the IP addresses from the result.

"""

from app import log, TIME_INTERVAL
from app.modules import mongodb
from app.modules import iptables
from apscheduler.schedulers.background import BackgroundScheduler


def expirer():
    """ Searching/cleaning expired sessions """
    db = mongodb.Connector()
    sessions = db.expire_sessions() # querying expired sessions
    if type(sessions) == list:
        if len(sessions) > 0:
            fw = iptables.Worker()
            counter = fw.del_rules(sessions) # deleting rules
            if type(counter) != int:
                log.error('%s %s %s', "scheduler", "expirer", "FAIL_IPTABLES")
    else:
        log.error('%s %s %s', "scheduler", "expirer", "FAIL_MONGODB")


sched = BackgroundScheduler(daemon=True)
sched.add_job(expirer, 'interval', seconds=TIME_INTERVAL)
sched.start()
