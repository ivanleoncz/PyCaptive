#!/usr/bin/python3

from datetime import datetime
from flask import Flask, request

from app.modules import logger

log = logger.config()

app = Flask(__name__)

# setting up logging of every request, except Status Code 500 (see if below...)
@app.after_request
def after_request(response):
    if response.status_code != 500:
        timestamp = datetime.now()
        log.error('%s %s %s %s %s %s',
                   timestamp, 
                   request.remote_addr, 
                   request.method, 
                   request.scheme, 
                   request.full_path, 
                   response.status)
    return response

from app.views import login
