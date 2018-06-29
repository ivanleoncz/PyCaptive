#!/usr/bin/python3
""" Main application module. """

from datetime import datetime
from flask import Flask, request
from app.modules import logger

log = logger.config()

from app.modules import scheduler

app = Flask(__name__)


@app.after_request
def after_request(response):
    """ Logging every request, except return code 500. """
    if response.status_code != 500:
        timestamp = datetime.now()
        log.error('[%s] %s %s %s %s %s %s',
                   timestamp,
                   "REQUEST",
                   request.method, 
                   request.scheme, 
                   request.full_path, 
                   request.remote_addr, 
                   response.status)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


from app.views import login
from app.views import welcome
