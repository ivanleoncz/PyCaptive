#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

@app.route("/")
def f_index():
    return "Flask Running!"

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=14900)
