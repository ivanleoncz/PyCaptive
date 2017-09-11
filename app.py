#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def f_index():
    header = request.headers
    return "Flask Running!<br><br>Request Headers:<br>%s" % header

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=14900)
