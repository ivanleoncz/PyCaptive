#!/usr/bin/python3

from glob import glob
import os
from subprocess import call
import sys

def add_ip(acl_file, ip):
    with open(acl_file, "r+") as f:
        f.seek(0,2)
        f.write("\n" + ip)
    return "Done!"

def del_ip(acl_file, ip):
    with open(acl_file,"r+") as f:
        for line in f.readlines():
            if ip not in line:
                f.write(line)
    return "Done!"

def read_acl(acl_file):
    with open(acl_file,"r") as f:
        print("\n----- IPs ------")
        for line in f.readlines():
            print(line,end="")
        print("\n----------------\n")
    return "Done!"

def list_acls():
    acls = glob("*.acl")
    if len(acls) == 0:
        print("NO ACLs WERE FOUND!")
    else:
        print("\n----- ACLs -----")
        for acl in acls:
            print(acl,end="")
        print("\n----------------\n")
    return "Done!"

try:
    while True:
        call(['clear'])
        print("\n=================================")
        print("========== ACL UPDATER ==========")
        print("=================================\n")
        print("1. Modify ACL")
        print("2. Read ACL")
        print("3. List ACLs")
        print("4. Exit\n")
        opt = input("Option: ")
        # modify ACL
        if opt == "1":
            call(['clear'])
            flag = "0"
            while flag == "0":
                print("\n\n$ MODIFY\n")
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
                        acl = input("ACL Name: ")
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
                        acl = input("ACL Name: ")
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
            print("\n\n$ READ\n")
            acls = glob("*.acl")
            if len(acls) == 0:
                print("NO ACLs WERE FOUND!\n")
                input("Press any key to continue...\n")
            else:
                for f in acls:
                    print(f, end="")
                acl = input("\n\nACL Name: ")
                if os.path.isfile(acl):
                    read_acl(acl)
                    input("Press any key to continue...\n")
                else:
                    print("ACL NOT FOUND!")
                    input("Press any key to continue...\n")

        # list ACLs
        elif opt == "3":
            call(['clear'])
            print("\n\n$ LIST\n")
            input("Press any key to continue...\n")
            list_acls()

        # exit...
        elif opt == "4":
            print("\nBye!\n")
            sys.exit(0)
        else:
            print("Wrong Option!")
            input("Press any key to continue...\n")

except KeyboardInterrupt:
    print("\n\nInterrupted!\n")
