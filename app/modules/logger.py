""" Global logging configuration. """

from logging.handlers import TimedRotatingFileHandler as tr_fh

from app import logger_dict as d

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
        if d.get("LOG_ROTATE_OS") == True:
            # log rotation performed by the OS service
            handler = logging.FileHandler(d.get("LOG_FILE"))
        else:
            # log rotation perfomed via logging (see pycaptive_settings.py)
            handler = tr_fh(d.get("LOG_FILE"),
                       when=d.get("LOG_ROTATE_WHEN"),
                backupCount=d.get("LOG_ROTATE_COUNT"))
        handler.setFormatter(log_form)
        conf.addHandler(handler)

    return conf
