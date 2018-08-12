#!/usr/bin/python3
""" Main application module. """

from flask import Flask
from app.modules import logger

log = logger.config()

from app.modules import scheduler

app = Flask(__name__)
app.config.from_pyfile('flask_settings.cfg')

@app.after_request
def after_request(response):
    """ Setting response headers for every request. """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


from app.views import login
from app.views import welcome
