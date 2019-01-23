#!/usr/bin/python3
""" Main application module. """
from flask.logging import default_handler
from flask import Flask, abort, redirect, request, render_template, session
import logging.config

# setup flask
app = Flask(__name__)

app.config.from_object('app.settings')
app.config.from_envvar('PYCAPTIVE_SETTINGS', silent=True)

# setup logging
app.logger.removeHandler(default_handler)
logging.config.dictConfig(app.config['LOGGING'])

# scheduler
from app.modules import scheduler

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
