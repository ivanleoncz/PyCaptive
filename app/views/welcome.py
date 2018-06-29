#!/usr/bin/env python3
""" Module for /login view/route."""

from flask import render_template

from app import app

@app.route("/welcome")
def f_welcome():
    return render_template("welcome.html")
