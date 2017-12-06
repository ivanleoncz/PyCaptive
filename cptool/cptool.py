#!/usr/bin/python3

import os
import sys

import import_export
import usermgmt


imp = "import_users.csv"
exp = "export_users.csv"


def helper():
    """ TODO: create export and edit functions... """
    print("\n[Captive Portal Tool]\n\nOptions:")
    print("    --import:  import users [.csv -> database]")
    print("    --export:  export users [database -> .csv]")
    print("    --search:  search user")
    print("    --create:  create user")
    print("    --remove:  remove user")
    print("    --update:  update user")
    print("\nExample:\n     python3",sys.argv[0],"--create\n")


if __name__ == "__main__":
    args = len(sys.argv)
    if args == 1 or args > 2:
        helper()
    else:
        transfer = import_export.Transfer()
        user = usermgmt.Users()
        if sys.argv[1] == "--import":
            if os.path.isfile(imp):
                transfer.import_users(imp)
        elif sys.argv[1] == "--export":
            if os.path.isfile(exp):
                transfer.export_users(exp)
            transfer.export_users(exp)
        elif sys.argv[1] == "--search":
            opt = input("\n1. Full Data\n2. Normal\n\n> (Ex.: 1) ")
            if opt == "1":
                user.find_users("full")
            elif opt == "2":
                user.find_users("normal")
            else:
                print("Wrong Option!")
        elif sys.argv[1] == "--create":
            user = usermgmt.Users()
            user.create()
        elif sys.argv[1] == "--remove":
            user = usermgmt.Users()
            user.remove()
        elif sys.argv[1] == "--update":
            user = usermgmt.Users()
            user.update()
        else:
            helper()

