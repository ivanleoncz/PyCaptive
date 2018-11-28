#!/usr/bin/python3

""" PyCaptive: Test Mode """

if __name__ == "__main__":
    from app import app, TEST
    from termcolor import colored
    print("\n PyCaptive Test Mode \n")
    if TEST is True:
        msg = " INFO: for Flask debug, see app/flask_settings.cfg\n"
        print(colored( msg, "green"))
        try:
            app.run(host="0.0.0.0", port=5000)
        except KeyboardInterrupt:
            print("Interrupted!")
        except Exception as e:
            print("Exception:", e)
    else:
        msg = " INFO: must set TEST flag on app/pycaptive_settings.py as True\n"
        print(colored(msg, "yellow"))
