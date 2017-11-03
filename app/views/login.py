#!/usr/bin/env python3
""" Module for /login view/route."""

from app import app

print("Module Loaded: views.login")

@app.route("/login", methods=['GET','POST'])
def f_login():
    """ Processing request. """
    from flask import abort, render_template, request
    from app.modules import iptables, logger, mongodb
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ipaddress = request.remote_addr
        logs = logger.Logger()
        log = logs.config()
        mc = mongodb.Connector()
        login = mc.login(username,password)
        if login == 0:
            login_record = mc.add_record(username,ipaddress)
            if login_record == 0:
                fw = iptables.Worker()
                allow = fw.test_add_rule(ipaddress)
                if allow == 0:
                    return "<h1> Login Successful! </h1>"
                else:
                    log.error('%s:%s',"Exception",allow)
                    return "fail..."
            else:
                log.error('%s:%s',"Exception",login_record)
                return "fail..."
        elif login == 1 or login == 2:
            message = "Check Your Credentials..."
            return render_template("login.html",login_failed=message)
        else:
            log.error('%s:%s',"Exception",login)
            return "fail..."
    else:
        # 405: Method Not Allowed
        abort(405)

