#!/usr/bin/python3

""" Application main module. """

import os

if os.getuid() == 0:
    from app import app
    app.config['MAX_CONTENT_LENGTH']=128000
    if __name__ == "__main__":
        print("\nPyCaptive is running (standalone).\n")
        app.run(host="0.0.0.0",port=14900)
    else:
        print("\nCannot be imported!\n\nRun: sudo ./standalone.py\n")
else:
    print("\nMust have root privileges!\n\nRun: sudo ./standalone.py\n")
    
