#!/usr/bin/python3

""" Module for logging configuration. """

import logging
from logging.handlers import RotatingFileHandler

class Logger:
    """ Logger configuration. """

    def config(self):
        """ Setting up. """
        conf = logging.getLogger('__name__')
        if not conf.handlers: # this if, avoid multiple execution of log messages
            conf.setLevel(logging.ERROR)
            file_path = "/var/log/captive_portal.log"
            handler = RotatingFileHandler(file_path, maxBytes=50000000, backupCount=5)
            conf.addHandler(handler)
        return conf



