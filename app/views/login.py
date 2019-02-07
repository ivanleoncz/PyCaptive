""" Module for /login view/route."""

from user_agents import parse

from app import app, abort, redirect, render_template, request, session
from app.modules import iptables
from app.modules import mongodb
import logging

LOGGER = logging.getLogger(__name__)

__author__ = "@ivanleoncz"


@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def f_login():
    """ Processing request. """
    # Verifies if the request was transmited via Proxy or not.
    client_ip = None
    if request.environ.get('HTTP_X_REAL_IP') is not None:
        client_ip = request.environ.get('HTTP_X_REAL_IP')
    else:
        client_ip = request.environ.get('REMOTE_ADDR')

    if request.method == 'GET':
        LOGGER.info('%s %s %s', "/login", "GET", client_ip)
        return render_template("login.html")
    elif request.method == 'POST':
        LOGGER.info('%s %s %s', "/login", "POST", client_ip)
        user_data = user_data_parser(request.headers.get('User-Agent'))
        username = request.form['username']
        password = request.form['password']
        db = mongodb.Connector()
        login = db.login(username, password)
        if login == 0:
            session_id = db.add_session(username, client_ip, user_data)
            if len(str(session_id)) == 24:
                fw = iptables.Worker()
                allow = fw.add_rule(client_ip)
                if allow == 0:
                    LOGGER.info('%s %s %s', "login", "OK", client_ip)
                    session["SessionID"] = str(session_id)
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
    devices["PC"] = ua.is_pc
    devices["Smartphone"] = ua.is_mobile
    devices["Tablet"] = ua.is_tablet
    # functions for determining Unknown brand or family for a device
    brand = lambda x: "Unknown" if x is None else ua.device.brand
    family = lambda x: "Unknown" if x is "Other" else ua.device.family
    # building user_data (device detection via list comprehension )
    user_data = {}
    user_data["device"] = [k for k,v in devices.items() if v][0]
    user_data["brand"] = brand(ua.device.brand)
    user_data["family"] = family(ua.device.family)
    user_data["os"] = ua.os.family
    user_data["browser"] = ua.browser.family
    return user_data
