""" Global logging configuration. """

from logging.handlers import TimedRotatingFileHandler as tr_fh

from app import LOG_FILE, LOG_ROTATE, LOG_ROTATE_WHEN, LOG_ROTATE_COUNT

__author__ = "@ivanleoncz"

import logging

def config():
    """ Setting up log configuration. """

    conf = logging.getLogger(__name__)

    # avoids multiple log messages
    if not conf.handlers:
        conf.setLevel(logging.INFO)
        log_form = logging.Formatter('%(asctime)s [%(levelname)s]\t%(message)s')
        handler = None
        if LOG_ROTATE == True:
            # configuring log rotation (see pycaptive_settings.py)
            handler = tr_fh(LOG_FILE,
                       when=LOG_ROTATE_WHEN, backupCount=LOG_ROTATE_COUNT)
        elif LOG_ROTATE == False:
            # no log rotation will be performed, leaving to OS (logorotate)
            handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(log_form)
        conf.addHandler(handler)

    return conf
