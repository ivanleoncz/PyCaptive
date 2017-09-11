#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def f_index():
    remote_ip = request.remote_addr
    headers = request.headers
    return "Flask Running!<br><br>Remote IP: %s<br>Request Headers: %s" % (remote_ip,headers)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=14900)
