#!/usr/bin/python3

""" PyCaptive: Standalone Mode """

from app.global_settings import HOST, PORT


if __name__ == "__main__":
    from app import app
    print("\n PyCaptive Standalone Mode\n")
    print(" \033[1;34mINFO\033[1;m: I was designed for test purposes only.\n")
    try:
        app.run(host=HOST, port=PORT)
    except KeyboardInterrupt:
        print("Interrupted!")
    except Exception as e:
        print("Exception:", e)
