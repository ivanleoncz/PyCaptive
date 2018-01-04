#!/usr/bin/python3

""" Application main module. """

import os

if os.getuid() == 0:
    from app import app
    app.config.from_object('config')
    if __name__ == "__main__":
        app.run(host="0.0.0.0",port=14900)
    else:
        print("\nIt's a script, not a module!\n    Ex.: sudo python3 run.py\n")
else:
    print("\nMust have root privileges!\n    Ex.: sudo python3 run.py\n")
    
