#!/usr/bin/python3

""" PyCaptive: Standalone Mode (Werkzeug) """

__author__ = "@ivanleoncz"

import os


if os.getuid() == 0:
    if __name__ == "__main__":
        from app import app
        print("\nPyCaptive is running (Standalone: Werkzeug).\n")
        try:
            app.config['MAX_CONTENT_LENGTH']=128000
            app.run(host="0.0.0.0",port=14900)
        except KeyboardInterrupt:
            print("Interrupted!")
        except Exception as e:
            print("Exception:", e)
    else:
        print("\nCannot be imported!\n\nRun: sudo ./pycaptive_werkzeug.py\n")
else:
    print("\nMust have root privileges!\n\nRun: sudo ./pycaptive_werkzeug.py\n")
    
