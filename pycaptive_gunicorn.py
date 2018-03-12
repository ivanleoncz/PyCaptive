#!/usr/bin/python3

""" PyCaptive Standalone (Gunicorn). 

NOTICE: do not use it on production environments.
"""

__author__ = "@ivanleoncz"

import os


if os.getuid() == 0:
    if __name__ == "__main__":
        import subprocess as sp
        print("\nPyCaptive is running (Standalone: Gunicorn).\n")
        try:
            command = ["gunicorn", "--name", "gunicorn_master", "--bind", "0.0.0.0:14900", 
                      "--user", "root", "--group", "root", 
                       "--workers", "4", "--pythonpath", ".", "wsgi"]
            sp.call(command)
        except KeyboardInterrupt:
            print("Interrupted!")
        except Exception as e:
            print("Exception:", e)
    else:
        print("\nCannot be imported!\n\nRun: sudo ./pycaptive_gunicorn.py\n")
else:
    print("\nMust have root privileges!\n\nRun: sudo ./pycaptive_gunicorn.py\n")

