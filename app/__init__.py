#!/usr/bin/python3
""" Main application module. """
import configparser
import os
import logging
import sys

from flask import Flask, abort, redirect, request, render_template, session

# Logging
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('pycaptive')
logger.setLevel(logging.INFO)


# PyCaptive configuration via .ini file
logger.info("detecting and loading pycaptive.ini")
config = configparser.ConfigParser()
paths = ('/etc/pycaptive/pycaptive.ini', 'app/pycaptive.ini', 'pycaptive.ini')
for ini in paths:
    if os.path.isfile(ini):
        logger.info(f"configuration file {os.path.abspath(ini)}")
        config.read(ini)
        break


# Generating dict based on pycaptive.ini for loading into Flask app.config
if config.sections():
    ini_dict = {}
    for section in config:
        for opt in list(config[section]):
            if section in ini_dict:
                ini_dict[section][opt] = config[section][opt]
            else:
                ini_dict[section] = {opt: config[section][opt]}
else:
    logger.error("no pycaptive.ini file was found. Aborting!")
    sys.exit()


# Flask Setup
app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PYCAPTIVE'] = ini_dict


# Scheduler
from app.modules import scheduler

# Views
from app.views import login, welcome

@app.route("/test")
def f_test():
    return "PyCaptive is running!"
