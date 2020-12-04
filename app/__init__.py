#!/usr/bin/python3
""" Main application module. """
import os
import sys

from flask import Flask, abort, redirect, request, render_template, session

from app.modules import helper

logger = helper.configure_logging()
ini = helper.search_and_load_ini()

if not ini:
    logger.error("no pycaptive.ini file was found. Aborting!")
    sys.exit()


# This is for 'gen_config_files.py' only. It scapes the whole import cycle which
# is performed when loading the application and all other requirements involved
# on PyCaptive, when gen_config_files.py is called by install.sh, since that
# no extra package (requirements.txt) is needed during the installation process.
if "gen_config_files" not in str(sys.modules['__main__']):

    # Flask Setup
    app = Flask(__name__)
    app.config['DEBUG'] = False
    app.config['SECRET_KEY'] = os.urandom(24)

    # Scheduler
    from app.modules import scheduler

    # Views
    from app.views import login, welcome

