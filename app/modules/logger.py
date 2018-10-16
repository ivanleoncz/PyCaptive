""" Global logging configuration. """

from logging.handlers import TimedRotatingFileHandler

__author__ = "@ivanleoncz"

import logging

def config():
    """ Setting up log configuration. """
    log_f = "/var/log/pycaptive/pycaptive.log"
    conf = logging.getLogger(__name__)
    if not conf.handlers: # avoids multiple log messages
        conf.setLevel(logging.ERROR)
        handler = TimedRotatingFileHandler(log_f, when='midnight', backupCount=52)
        conf.addHandler(handler)
    return conf
