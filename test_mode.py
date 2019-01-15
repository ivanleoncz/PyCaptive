#!/usr/bin/python3

""" PyCaptive: Test Mode """

if __name__ == "__main__":
    from app import app, TEST_MODE
    from termcolor import colored
    print("\n PyCaptive Test Mode \n")
    if TEST_MODE is True:
        try:
            msg = " INFO: running PyCaptive (Test Mode)\n"
            print(colored(msg, "green"))
            app.run(host="0.0.0.0", port=5000)
        except KeyboardInterrupt:
            print("Interrupted!")
        except Exception as e:
            msg = "Exception: " + e
            print(colored(msg, "red"))
    else:
        msg = " INFO: must set TEST flag as True (see pycaptive_settings.py)\n"
        print(colored(msg, "red"))
