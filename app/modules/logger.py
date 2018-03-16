#!/usr/bin/python3
""" Global logging configuration. """

import logging
from logging.handlers import RotatingFileHandler

def config():
    """ Setting up log configuration. """
    conf = logging.getLogger(__name__)
    if not conf.handlers: # avoids multiple log messages
        conf.setLevel(logging.ERROR)
        file_path = "/var/log/pycaptive.log"
        handler = RotatingFileHandler(file_path, maxBytes=50000000, backupCount=5)
        conf.addHandler(handler)
    return conf
