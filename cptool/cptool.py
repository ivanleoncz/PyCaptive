#!/usr/bin/python3

import sys

import database
import usermgmt


def helper():
    print("\n[Captive Portal Tool]\n")
    print("Options:")
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
        oper = database.MongoDB()
        user = usermgmt.Users()
        if sys.argv[1] == "--import":
            oper.import_users()
        elif sys.argv[1] == "--export":
            oper.export_users()
        elif sys.argv[1] == "--search":
            opt = input("\n1. Full Data\n2. Normal\n\n* (Ex.: 1): ")
            if opt == "1":
                user.search("full")
            elif opt == "2":
                user.search("normal")
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

