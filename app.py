#!/usr/bin/env python3

from apscheduler.schedulers.background import BackgroundScheduler
from flask import abort, Flask, render_template, request
from app_modules import mongodb
from app_modules import iptables

# this job could be the worker which will evaluate the expired sessions at MongoDB
def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=60)
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
        client_ip = request.remote_addr
        mc = mongodb.Connector(username,password,client_ip)
        login = mc.login()
        if login == "0x0000":
            firewall = iptables.Ruler(client_ip)
            allow = firewall.test_add_rule()
            if allow == "0x0000":
                return "<h1> Login Successful! </h1>"
            else:
                return "Error: %s" % allow 
        elif login == "0x0db2" or login == "0x0db3":
            message = "Check Your Credentials..."
            return render_template("login.html",login_failed=message)
        else:
            return "<h1> Return Code: %s </h1>" % login
    else:
        # 405: Method Not Allowed
        abort(405)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=14900)

