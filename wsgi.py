#!/usr/bin/python3

from app import app as application

application.config['MAX_CONTENT_LENGTH']=128000
