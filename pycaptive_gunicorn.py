#!/usr/bin/python3

""" PyCaptive Standalone (Gunicorn). """

__author__ = "@ivanleoncz"

import os


if os.getuid() == 0:
    if __name__ == "__main__":
        import subprocess as sp
        print("\nPyCaptive is running: Standalone Mode (Gunicorn)\n")
        print("\033[1;34mINFO\033[1;m: don't use it in production environents!\n")
        try:
            command = ["gunicorn", "--name", "gunicorn_master",
                                   "--bind", "0.0.0.0:14900",
                                   "--user", "root",
                                   "--group", "root",
                                   "--workers", "4",
                                   "--pythonpath", ".", "wsgi"]
            sp.call(command)
        except KeyboardInterrupt:
            print("Interrupted!")
        except Exception as e:
            print("Exception:", e)
else:
    print("\n\033[1;31mERROR\033[1;m: Must have root privileges!")
    print("Run:\n\t$ sudo ./pycaptive_gunicorn.py")

