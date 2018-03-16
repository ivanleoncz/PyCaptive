#!/usr/bin/python3
""" Global logging configuration. """

from logging.handlers import RotatingFileHandler

__author__ = "@ivanleoncz"

import logging

def config():
    """ Setting up log configuration. """
    conf = logging.getLogger(__name__)
    if not conf.handlers: # avoids multiple log messages
        conf.setLevel(logging.ERROR)
        f = "/var/log/pycaptive.log"
        handler = RotatingFileHandler(f, maxBytes=50000000, backupCount=5)
        conf.addHandler(handler)
    return conf
