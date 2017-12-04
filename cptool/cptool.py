#!/usr/bin/python3

import os
import sys

import import_export
import create_remove

imp = "import_users.csv"
exp = "export_users.csv"


def helper():
    """ TODO: create export and edit functions... """
    print("\n[Captive Portal Tool]\n\nOptions:")
    print("    --import:  import users [.csv -> database]")
    print("    --export:  export users [database -> .csv]")
    print("    --create:  create user")
    print("    --remove:  remove user")
    print("\nExample:\n     python3",sys.argv[0],"--create\n")


if __name__ == "__main__":
    args = len(sys.argv)
    if args == 1 or args > 2:
        helper()
    else:
        if sys.argv[1] == "--import":
            if os.path.isfile(imp):
                transfer = import_export.Transfer()
                transfer.import_users(imp)
        elif sys.argv[1] == "--export":
            transfer = import_export.Transfer()
            transfer.export_users(exp)
        elif sys.argv[1] == "--create":
            user = create_remove.Users()
            user.create()
        elif sys.argv[1] == "--remove":
            user = create_remove.Users()
            user.remove()
        else:
            helper()

