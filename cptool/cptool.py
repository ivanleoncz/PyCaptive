#!/usr/bin/python3

import os
import subprocess as sp
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
    print("    --expire:  expire session")
    print("     --check:  checking user credentials")
    print("      --help:  this help")
    print("\nExample:\n    sudo python3",sys.argv[0],"--create\n")
    print("Important:\n    Always execute it using root privileges (sudo)!\n ")


if __name__ == "__main__":
    if os.getuid() == 0:
        args = len(sys.argv)
        if args == 1 or args > 2:
            helper()
        else:
            if sys.argv[1] == "--import":
                sp.call(['clear'])
                oper = database.MongoDB()
                oper.import_users()
            elif sys.argv[1] == "--export":
                sp.call(['clear'])
                oper = database.MongoDB()
                oper.export_users()
            elif sys.argv[1] == "--search":
                sp.call(['clear'])
                user = usermgmt.Users()
                opt = input("\n* Full or Normal Data (f/n): ")
                if opt == "f":
                    user.search("full")
                elif opt == "n":
                    user.search("normal")
                else:
                    print("\nWrong Option!\n")
            elif sys.argv[1] == "--create":
                sp.call(['clear'])
                user = usermgmt.Users()
                user.create()
            elif sys.argv[1] == "--remove":
                sp.call(['clear'])
                user = usermgmt.Users()
                user.remove()
            elif sys.argv[1] == "--update":
                sp.call(['clear'])
                user = usermgmt.Users()
                user.update()
            elif sys.argv[1] == "--expire":
                sp.call(['clear'])
                oper = database.MongoDB()
                oper.expire_session()
            elif sys.argv[1] == "--check":
                sp.call(['clear'])
                user = usermgmt.Users()
                user.check_credentials()
            elif sys.argv[1] == "--help":
                helper()
            else:
                helper()
    else:
        helper()

