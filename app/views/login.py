""" Module for /login view/route."""

from flask import abort, redirect, render_template, request, url_for
from datetime import datetime
from user_agents import parse

from app import app, log
from app.modules import iptables
from app.modules import mongodb


@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def f_login():
    """ Processing request. """
    client_ip = None
    if request.method == 'GET':
        # Verifies if the request was transmited via Proxy,
        # in order to adapt the Standalone execution.
        if request.environ.get('HTTP_X_REAL_IP') is not None:
            client_ip = request.environ.get('HTTP_X_REAL_IP')
        else:
            client_ip = request.environ.get('REMOTE_ADDR')
        ts = datetime.now()
        log.error('[%s] %s %s %s %s', ts, "/login", "GET", client_ip, "OK")
        return render_template("login.html")
    elif request.method == 'POST':
        user_data = user_data_parser(request.headers.get('User-Agent'))
        username = request.form['username']
        password = request.form['password']
        db = mongodb.Connector()
        login = db.login(username, password)
        if login == 0:
            login_record = db.add_session(username, client_ip, user_data)
            if login_record == 0:
                fw = iptables.Worker()
                allow = fw.add_rule(client_ip)
                if allow == 0:
                    return redirect("/welcome")
                else:
                    msg = "Server Error (firewall)"
                    return render_template("login.html", login_msg=msg)
            else:
                msg = "Server Error (session)"
                return render_template("login.html", login_msg=msg)
        elif login == 1 or login == 2:
            msg = "Wrong Credentials!"
            return render_template("login.html", login_msg=msg)
        else:
            msg = "Server Error (login)"
            return render_template("login.html", login_msg=msg)
    else:
        abort(405) # 405: Method Not Allowed


def user_data_parser(request_ua):
    ua = parse(request_ua)
    # checking device presence (True/False)
    devices = {}
    devices["pc"] = ua.is_pc
    devices["mobile"] = ua.is_mobile
    devices["tablet"] = ua.is_tablet
    # functions for determining Unknown brand or family for a device
    brand = lambda x: "Unknown" if x is None else ua.device.brand
    family = lambda x: "Unknown" if x is "Other" else ua.device.family
    # building user_data (device detection via list comprehension )
    user_data = {}
    user_data["device"] = [k for k,v in devices.items() if v == True][0]
    user_data["brand"] = brand(ua.device.brand)
    user_data["family"] = family(ua.device.family)
    user_data["os"] = ua.os.family
    user_data["browser"] = ua.browser.family
    return user_data
