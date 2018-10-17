""" Global logging configuration. """

from logging.handlers import TimedRotatingFileHandler as tr_fh

from app import LOG_FILE, LOG_ROTATE, LOG_ROTATE_WHEN, LOG_ROTATE_COUNT

__author__ = "@ivanleoncz"

import logging

def config():
    """ Setting up log configuration. """

    conf = logging.getLogger(__name__)
    if not conf.handlers: # avoids multiple log messages
        conf.setLevel(logging.INFO)
        log_form = logging.Formatter('%(asctime)s [%(levelname)s]\t%(message)s')
        handler = None
        if LOG_ROTATE == True:
            #  logging module will rotate the log files
            handler = tr_fh(LOG_FILE,
                       when=LOG_ROTATE_WHEN, backupCount=LOG_ROTATE_COUNT)
        elif LOG_ROTATE == False:
            # no rotation will be performed, leaving rotation to OS tool
            handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(log_form)
        conf.addHandler(handler)
    return conf
