#!/usr/bin/env python3

import bcrypt
from getpass import getpass
from flask import abort, Flask, render_template, request
from app_modules import mongodb

app = Flask(__name__)

def password_check(passwd):
    salt = bcrypt.gensalt()
    password = "Yougotit*88".encode('utf-8')
    hashed = bcrypt.hashpw(password,salt)
    new_hashed = bcrypt.hashpw(passwd.encode('utf-8'),hashed)
    if new_hashed == hashed:
        return "ok"

@app.route("/")
def f_index():
    remote_ip = request.remote_addr
    headers = request.headers
    return "Flask Running!<br><br>Remote IP: %s<br>Request Headers: %s" % (remote_ip,headers)

@app.route("/login", methods=['GET','POST'])
def f_login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("POST Username:",username)
        print("POST Password:",password)
        mc = mongodb.Connector(username,password)
        login = mc.login()
        if login == "ok":
            return "<h1> Login Successful!!! </h1>"
        elif login == "nok":
            return "<h1> Wrong Password... </h1>"
        else:
            return "<h1> Database Timeout! </h1>"
    else:
        # 405: Method Not Allowed
        abort(405)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=14900)
