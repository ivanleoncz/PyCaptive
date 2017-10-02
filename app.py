#!/usr/bin/env python3

import bcrypt
from getpass import getpass
from flask import abort, Flask, render_template, request

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
        name = request.form['username']
        passwd = request.form['password']
        check = password_check(passwd)
        if check == "ok":
            return "Login Successful!!!"
        else:
            return "Wrong Password..."
    else:
        # 405: Method Not Allowed
        abort(405)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=14900)
