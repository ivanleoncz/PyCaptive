#!/usr/bin/python3
""" Main application module. """

from app.modules import logger
from app.modules import scheduler
from datetime import datetime
from flask import Flask, request

log = logger.config()
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
    return response

from app.views import login
