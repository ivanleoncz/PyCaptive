#!/usr/bin/python3

import os
import subprocess as sp
import sys

import database
import usermgmt


if __name__ == "__main__":
    if os.getuid() == 0:
        print("\n[PyCaptive Tool]\n")
        print("1. Create User")
        print("2. Remove User")
        print("3. Update User")
        print("4. Search User")
        print("5. Import Users [csv -> database] ")
        print("6. Export Users [database -> csv]")
        print("7. Check User Credential")
        print("8. Expire Active Session")
        print("0. Exit\n")
        opt = input("> ")
        if opt == "1":
            sp.call(['clear'])
            user = usermgmt.Users()
            user.create()
        elif opt == "2":
            sp.call(['clear'])
            user = usermgmt.Users()
            user.remove()
        elif opt == "3":
            sp.call(['clear'])
            user = usermgmt.Users()
            user.update()
        elif opt == "4":
            user = usermgmt.Users()
            opt = input("\n* Full or Normal Data (f/n): ")
            if opt == "f":
                sp.call(['clear'])
                user.search("full")
            elif opt == "n":
                sp.call(['clear'])
                user.search("normal")
            else:
                print("\nWrong Option!\n")
        elif opt == "5":
            sp.call(['clear'])
            oper = database.MongoDB()
            oper.import_users()
        elif opt == "6":
            sp.call(['clear'])
            oper = database.MongoDB()
            oper.export_users()
        elif opt == "7":
            sp.call(['clear'])
            user = usermgmt.Users()
            user.check_credentials()
        elif opt == "8":
            sp.call(['clear'])
            oper = database.MongoDB()
            oper.expire_session()
        elif opt == "0":
            print("\nBye!\n")
        else:
            print("\nWrong Option!\n")
    else:
        print("\nMust have root privileges!\n\nRun: sudo ./pycaptool.py\n")
else:
    print("\nCannot be imported!\n\nRun: sudo ./pycaptool.py\n")

