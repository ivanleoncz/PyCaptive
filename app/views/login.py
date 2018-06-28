#!/usr/bin/env python3
""" Module for /login view/route."""

from datetime import datetime, timedelta
from flask import abort, redirect, render_template, request, url_for

from app import app
from app.modules import iptables
from app.modules import mongodb


@app.route("/login", methods=['GET', 'POST'])
def f_login():
    """ Processing request. """
    client_ip = request.headers['X-Real-IP']
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = mongodb.Connector()
        login = db.login(username, password)
        if login == 0:
            login_record = db.add_session(username, client_ip)
            if login_record == 0:
                fw = iptables.Worker()
                allow = fw.add_rule(client_ip)
                if allow == 0:
                    return redirect(url_for('f_welcome', usr=username))
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

@app.route("/welcome/<usr>")
def f_welcome(usr):
    login_time  = datetime.now()
    expire_time = login_time + timedelta(hours=12)
    expire_time = expire_time.strftime('%H:%M')
    return render_template("welcome.html", username=usr, time=expire_time)
