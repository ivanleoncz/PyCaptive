#!/usr/bin/python3

from app import app as application

application.config.from_object('config')

if __name__ == "__main__":
    application.run(host="0.0.0.0",port=14901)
