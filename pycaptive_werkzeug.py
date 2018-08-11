#!/usr/bin/python3

""" PyCaptive: Standalone Mode (Werkzeug) """

__author__ = "@ivanleoncz"

import os


if os.getuid() == 0:
    if __name__ == "__main__":
        from app import app
        print("\nPyCaptive is running: Standalone Mode  (Werkzeug)\n")
        print("\033[1;34mINFO\033[1;m: don't use it in production environents!\n")
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
    print("\n\033[1;31mERROR\033[1;m: Must have root privileges!")
    print("Run:\n\t$ sudo ./pycaptive_werkzeug.py")
    
