#!/usr/bin/env python3

""" Scheduler for Login Sessions.  """

def ses(): # Session Expiration Scheduler
    """ Verifies expired sessions. """
    from app.modules import mongodb
    from app.modules import iptables
    from app.modules import logger
    logs = logger.Logger()
    log = logs.config()
    log.error("Running Scheduler!!!")
    mc = mongodb.Connector()
    expired_sessions = mc.del_records()
    if type(expired_sessions) == list:
        if len(expired_sessions) > 0:
            print("SCHEDULER: expired sessions - ", expired_sessions)
            log.error('%s:%s',"Expired Sessions",expired_sessions)
            fw = iptables.Worker()
            counter = fw.test_del_rule(expired_sessions)
            if type(counter) == int:
                if counter > 0:
                    print("SCHEDULER: removed rules - ", counter)
                    log.error('%s:%s',"Removed Rules",counter)
            else:
                log.error('%s:%s',"Exception",counter)
    else:
        log.error('%s:%s',"Exception",expired_sessions)

