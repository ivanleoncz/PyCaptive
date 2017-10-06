#!/usr/bin/env python3

from flask import abort, Flask, render_template, request
from app_modules import mongodb

app = Flask(__name__)

@app.route("/")
def f_index():
    """ Index route for test purposes."""
    remote_ip = request.remote_addr
    headers = request.headers
    return "Flask Running!<br><br>Remote IP: %s<br>Request Headers: %s" % (remote_ip,headers)

@app.route("/login", methods=['GET','POST'])
def f_login():
    """ Processing request. 
        
        GET: loading login interface
        POST: processing login request (form data)
    """
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mc = mongodb.Connector(username,password)
        login = mc.login()
        if login == 0:
            return "<h1> Login Successful! </h1>"
        elif login == 1 or login == 2:
            return render_template("login.html",login_failed="Check Your Credentials...")
        elif login == 2:
            return "<h1> Database Error... </h1>"
        else:
            return "<h1> Database Module Error... </h1>"
    else:
        # 405: Method Not Allowed
        abort(405)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=14900)
