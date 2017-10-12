#!/usr/bin/env python3

from flask import abort, Flask, render_template, request
from app_modules import mongodb
from app_modules import iptables

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
        mc = mongodb.Connector(username,password)
        login = mc.login()
        if login == "0x0000":
            firewall = iptables.Ruler(self.ipaddr)
            allow = firewall.test_rule()
            if allow == "0x0000":
                return "<h1> Login Successful! </h1>"
            else:
                return "Error: %s" % allow 
        elif login == "0x0db2" or login == "0x0db3":
            return render_template("login.html",login_failed="Check Your Credentials...")
        else:
            return "<h1> Return Code: %s </h1>" % login
    else:
        # 405: Method Not Allowed
        abort(405)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=14900)
