""" Module for /welcome view/route. """

from json import loads
from app import app, redirect, render_template, session
from app.modules import mongodb

__author__ = "@ivanleoncz"


@app.route("/welcome")
def f_welcome():
    if "SessionID" in session:
        db = mongodb.Connector()
        ua = db.check_session(session.get("SessionID"))
        ua["LoginTime"] = ua["LoginTime"].strftime("%H:%M:%S - (%d/%b/%Y)")
        ua["ExpireTime"] = ua["ExpireTime"].strftime("%H:%M:%S - (%d/%b/%Y)")
        session.pop("SessionID", None)
        return render_template("welcome.html", userdata=ua)
    else:
        return redirect("/login")
