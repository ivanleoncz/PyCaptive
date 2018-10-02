#!/usr/bin/python3

""" PyCaptive: Standalone Mode (Gunicorn) """

from app.custom_settings import HOST, PORT

__author__ = "@ivanleoncz"

host_port = HOST + ":" + str(PORT)

if __name__ == "__main__":
    import subprocess as sp
    print("\nPyCaptive is running: Standalone Mode (Gunicorn)\n")
    print("\033[1;34mINFO\033[1;m: don't use it on production environments!\n")
    try:
        command = ["gunicorn", "--name", "gunicorn_master",
                               "--bind", host_port,
                               "--user", "root",
                               "--group", "root",
                               "--workers", "4",
                               "--pythonpath", ".", "wsgi"]
        sp.call(command)
    except KeyboardInterrupt:
        print("Interrupted!")
    except Exception as e:
        print("Exception:", e)
