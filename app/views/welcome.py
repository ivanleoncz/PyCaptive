""" Module for /welcome view/route. """

from flask import render_template

from app import app

@app.route("/welcome")
def f_welcome():
    return render_template("welcome.html")
