#!/usr/bin/env python3

from flask import abort, Flask, request

app = Flask(__name__)

@app.route("/")
def f_index():
    remote_ip = request.remote_addr
    headers = request.headers
    return "Flask Running!<br><br>Remote IP: %s<br>Request Headers: %s" % (remote_ip,headers)

@app.route("/login", methods=['GET','POST'])
def f_login():
    if request.method == 'GET':
        return "Welcome to login page!"
    elif request.method == 'POST':
        name = request.form['username']
        passwd = request.form['password']
        return "Processing login!"
    else:
        # 405: Method Not Allowed
        abort(405)


if __name__ == "__main__":
    app.run(host="127.0.0.1",port=14900)
