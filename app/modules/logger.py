#!/usr/bin/python3

import logging
from logging.handlers import RotatingFileHandler

class Logger:

    def config(self):
        conf = logging.getLogger('__name__')
        if not conf.handlers:
            conf.setLevel(logging.ERROR)
            file_path = "/var/log/captive_portal.log"
            handler = RotatingFileHandler(file_path, maxBytes=50000000, backupCount=5)
            conf.addHandler(handler)
        return conf



