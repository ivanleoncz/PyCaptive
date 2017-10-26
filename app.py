#!/usr/bin/env python3

from apscheduler.schedulers.background import BackgroundScheduler
from flask import abort, Flask, render_template, request
import logging
from logging.handlers import RotatingFileHandler
from app_modules import mongodb
from app_modules import iptables

# SES (Session Expiration Scheduler)
def se_scheduler():
    """ Verifies expired sessions. """
    logger.error('%s',"Scheduler is alive!")
    mc = mongodb.Connector()
    expired_sessions = mc.del_records()
    if type(expired_sessions) == list:
        expired_len = len(expired_sessions)
        if expired_len > 0:
            logger.error('%s:%s',"Expired Sessions",expired_sessions)
            fw = iptables.Worker()
            counter = fw.test_del_rule(expired_sessions)
            if type(counter) == int:
                if counter > 0:
                    logger.error('%s:%s',"Removed Rules",counter)
            else:
                logger.error('%s:%s',"Exception",counter)
    else:
        logger.error('%s:%s',"Exception",expired_sessions)
        
sched = BackgroundScheduler(daemon=True)
sched.add_job(se_scheduler,'interval',seconds=60)
sched.start()


app = Flask(__name__)

@app.route("/")
def f_index():
    """ Index route for test purposes."""
    remote_ip = request.remote_addr
    headers = request.headers
    return "Flask Running!<br><br>Remote IP: %s<br>Request Headers: %s" % (remote_ip,headers)

@app.route("/login", methods=['GET','POST'])
def f_login():
    """ Processing request. """
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ipaddress = request.remote_addr
        # process login
        mc = mongodb.Connector()
        login = mc.login(username,password)
        if login == 0:
            # process login record
            login_record = mc.add_record(username,ipaddress)
            if login_record == 0:
                # process firewall rule
                firewall = iptables.Worker()
                allow = firewall.test_add_rule(ipaddress)
                if allow == 0:
                    return "<h1> Login Successful! </h1>"
                else:
                    logger.error('%s:%s',"Exception",allow)
                    return "fail..."
            else:
                logger.error('%s:%s',"Exception",login_record)
                return "fail..."
        elif login == 1 or login == 2:
            message = "Check Your Credentials..."
            return render_template("login.html",login_failed=message)
        else:
            logger.error('%s:%s',"Exception",login)
            return "fail..."
    else:
        # 405: Method Not Allowed
        abort(405)

if __name__ == "__main__":
    handler = RotatingFileHandler('captive_portal.log',maxBytes=50000000, backupCount=5)
    logger = logging.getLogger('__name__')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    app.run(host="127.0.0.1",port=14900)
