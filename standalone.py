#!/usr/bin/python3

""" PyCaptive: Standalone Mode """

from app.custom_settings import HOST, PORT

__author__ = "@ivanleoncz"

if __name__ == "__main__":
    from app import app
    print("\nPyCaptive Standalone Mode  (Werkzeug)\n")
    print("\033[1;34mINFO\033[1;m: designed for test purposes only.\n")
    try:
        app.run(host=HOST, port=PORT)
    except KeyboardInterrupt:
        print("Interrupted!")
    except Exception as e:
        print("Exception:", e)
