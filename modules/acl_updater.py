#!/usr/bin/python3

from glob import glob
import os
from subprocess import call
import sys



def add_ip(acl_file, ip):
    with open(acl_file, "r+") as f:
        f.seek(0,2)
        f.write(ip + "\n")
    return "Done!"


def del_ip(acl_file, ip):
    with open(acl_file,"r+") as f:
        new_f = f.readlines()
        f.seek(0)
        f.truncate()
        for line in new_f:
            if ip not in line:
                f.write(line)
    return "Done!"


def read_acl(acl_file):
    with open(acl_file,"r") as f:
        for line in f.readlines():
            print(line,end="")
    return "Done!"


def list_acls():
    acls = glob("*.acl")
    for acl in acls:
        print("-",acl,end="")
    return "Done!"


def check_acls():
    acls = glob("*.acl")
    if len(acls) != 0:
        return "ok"
    else:
        return "No ACLs were found!"


def check_file(acl):
    if os.path.isfile(acl):
        return "ok"
    else:
        return "ACL not found!"


try:
    while True:
        call(['clear'])
        print("\n=================================")
        print("========== ACL UPDATER ==========")
        print("=================================\n")
        print("1. Modify")
        print("2. Read")
        print("3. List")
        print("4. Exit\n")
        opt = input("Option: ")

        # MODIFY
        if opt == "1":
            flag = "0"
            while flag == "0":
                call(['clear'])
                print("\n\n\n$ MODIFY\n")
                check = check_acls()
                if check == "ok":
                    print("1. Add IP")
                    print("2. Del IP")
                    print("3. Exit\n")
                    oper = input("Option: ")
                    # > add IP
                    if oper == "1":
                        list_acls()
                        acl = input("\n\nACL Name: ")
                        check_acl = check_file(acl) 
                        if check_acl == "ok":
                            print("----------------")
                            read_acl(acl)
                            print("\n----------------\n")
                            ip = input("Add IP: ")
                            add_ip(acl,ip)
                            print("----------------")
                            read_acl(acl)
                            print("\n----------------\n")
                            input("Press any key to continue...\n")
                        else:
                            print("ACL NOT FOUND!\n")
                            input("Press any key to continue...\n")
                    # > del IP
                    elif oper == "2":
                        list_acls()
                        acl = input("\n\nACL Name: ")
                        check_acl = check_file(acl)
                        if check_acl == "ok":
                            print("----------------")
                            read_acl(acl)
                            print("\n----------------\n")
                            ip = input("Del IP: ")
                            del_ip(acl,ip)
                            print("----------------")
                            read_acl(acl)
                            print("\n----------------\n")
                            input("Press any key to continue...\n")
                        else:
                            print("ACL NOT FOUND!\n")
                            input("Press any key to continue...\n")
                    # > exit
                    elif oper == "3":
                        flag = "1"
                    else:
                        print("WRONG OPTION!")
                else:
                    print(check)

        # READ
        elif opt == "2":
            call(['clear'])
            print("\n\n\n$ READ\n")
            check = check_acls()
            if check == "ok":
                list_acls()
                acl = input("\n\nACL Name: ")
                check_acl = check_file(acl)
                if check_acl == "ok":
                    print("----------------")
                    read_acl(acl)
                    print("\n----------------\n")
                    input("Press any key to continue...\n")
                else:
                    print("ACL NOT FOUND!\n")
                    input("Press any key to continue...\n")
            else:
                print(check)

        # LIST
        elif opt == "3":
            call(['clear'])
            print("\n\n\n$ LIST\n")
            check = check_acls()
            if check == "ok":
                print("----------------")
                list_acls()
                print("\n----------------\n")
                input("Press any key to continue...\n")
            else:
                print(check)
                input("Press any key to continue...\n")

        # EXIT
        elif opt == "4":
            print("\nBye!\n")
            sys.exit(0)
        else:
            print("Wrong Option!\n")
            input("Press any key to continue...\n")

except KeyboardInterrupt:
    print("\n\nInterrupted!\n")
