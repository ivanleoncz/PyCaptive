""" Module for /welcome view/route. """

from flask import render_template

from app import app, session
from app.modules import mongodb

__author__ = "@ivanleoncz"


@app.route("/welcome")
def f_welcome():
    if "SessionID" in session:
        db = mongodb.Connector()
        user_data = db.check_session(session.get("Session_id"))
        session.pop("SessionID", None)
        return render_template("welcome.html", userdata=user_data)
    else:
        return redirect("/login")
