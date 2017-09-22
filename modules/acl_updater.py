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
        print("----------------")
        for line in f.readlines():
            print(line,end="")
        print("\n----------------")
    return "Done!"

def list_acls():
    acls = glob("*.acl")
    if len(acls) == 0:
        print("NO ACLs WERE FOUND!")
    else:
        print("\n[ACLs]")
        for acl in acls:
            print("-",acl,end="")
    return "Done!"

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
        # modify ACL
        if opt == "1":
            flag = "0"
            while flag == "0":
                call(['clear'])
                print("\n\n\n$ MODIFY\n")
                acls = glob("*.acl")
                if len(acls) == 0:
                    print("NO ACLs WERE FOUND!")
                    input("Press any key to continue...\n")
                    flag = "1"
                else:
                    print("1. Add IP")
                    print("2. Del IP")
                    print("3. Exit\n")
                    oper = input("Option: ")

                    # add IP
                    if oper == "1":
                        list_acls()
                        acl = input("\n\nACL Name: ")
                        if os.path.isfile(acl):
                            read_acl(acl)
                            ip = input("\nAdd IP: ")
                            add_ip(acl,ip)
                            read_acl(acl)
                            input("\nPress any key to continue...\n")
                        else:
                            print("ACL NOT FOUND!\n")
                            input("Press any key to continue...\n")

                    # del IP
                    elif oper == "2":
                        list_acls()
                        acl = input("\n\nACL Name: ")
                        if os.path.isfile(acl):
                            read_acl(acl)
                            ip = input("\nDel IP: ")
                            del_ip(acl,ip)
                            read_acl(acl)
                            input("\nPress any key to continue...\n")
                        else:
                            print("ACL NOT FOUND!\n")
                            input("Press any key to continue...\n")

                    # exit IP
                    elif oper == "3":
                        flag = "1"
                    else:
                        print("WRONG OPTION!")
        # read ACL
        elif opt == "2":
            call(['clear'])
            print("\n\n\n$ READ\n")
            acls = glob("*.acl")
            if len(acls) == 0:
                print("NO ACLs WERE FOUND!\n")
                input("Press any key to continue...\n")
            else:
                list_acls()
                acl = input("\n\nACL Name: ")
                if os.path.isfile(acl):
                    read_acl(acl)
                    input("\n\nPress any key to continue...\n")
                else:
                    print("ACL NOT FOUND!")
                    input("\nPress any key to continue...\n")

        # list ACLs
        elif opt == "3":
            call(['clear'])
            print("\n\n\n$ LIST\n")
            list_acls()
            input("\n\nPress any key to continue...\n")

        # exit...
        elif opt == "4":
            print("\nBye!\n")
            sys.exit(0)
        else:
            print("Wrong Option!\n")
            input("Press any key to continue...\n")

except KeyboardInterrupt:
    print("\n\nInterrupted!\n")
