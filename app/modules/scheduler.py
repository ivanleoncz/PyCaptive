""" APScheculer for monitoring expired sessions.  

Started when the module is imported, periodically performing
a sweep on MongoDB (see pycaptive_settings.py:TIME_INTERVAL),
searching for expired sessions (IPs).

The result is passed to iptables module, which eliminates
the rules associated with the IP addresses which are returned
via APScheduler.
"""

from apscheduler.schedulers.background import BackgroundScheduler

from app.modules import mongodb
from app.modules import iptables
from app import app
import logging

LOGGER = logging.getLogger(__name__)

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
                LOGGER.info('%s %s %s', "scheduler", "expirer", "OK")
            else:
                LOGGER.error('%s %s %s', "scheduler", "expirer", "FAIL_IPTABLES")

    else:
        LOGGER.error('%s %s %s', "scheduler", "expirer", "FAIL_MONGODB")


sched = BackgroundScheduler(daemon=True)
sched.add_job(expirer, 'interval', seconds=app.config['SCHEDULER_DICT']["INTERVAL"])
sched.start()
