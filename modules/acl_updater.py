#!/usr/bin/python3

from glob import glob
import os
from subprocess import call
import sys

def add_ip(acl_file, ip):
    print("Adding IP!")
    with open(acl_file, "r+") as f:
        f.seek(0,2)
        f.write("\n" + ip)
    return "DONE!"

def del_ip(acl_file, ip):
    print("Deleting IP!")
    with open(acl_file,"r+") as f:
        for line in f.readlines():
            if ip not in line:
                f.write(line)
    return "DONE!"

def read_acl(acl_file):
    with open(acl_file,"r") as f:
        for line in f.readlines():
            print(line, end="")
    return "DONE!"


while True:
    call(['clear'])
    print("\n\n=================================")
    print("========== ACL UPDATER ==========")
    print("=================================\n\n")
    print("1. Modify ACL")
    print("2. Read ACL")
    print("3. List ACLs")
    print("4. Exit\n")
    opt = input("> ")
    # modify ACL
    if opt == "1":
        call(['clear'])
        flag = "0"
        while flag == "0":
            print("\n\n>>>>>>>>>> MODIFY <<<<<<<<<<\n\n")
            acls = glob("*.acl")
            if len(acls) == 0:
                print("NO ACLs WERE FOUND!")
                input("\nPress any key to continue...\n")
                flag = "1"
            else:
                print("1. Add IP")
                print("2. Del IP")
                print("3. Exit")
                oper = input("\n> ")
                # add IP
                if oper == "1":
                    acl = input("\nACL Name: ")
                    if os.path.isfile(acl):
                        ip = input("IP Address: ")
                        add_ip(acl,ip)
                        input("\nPress any key to continue...\n")
                    else:
                        print("ACL NOT FOUND!")
                        input("\nPress any key to continue...\n")
                # del IP
                elif oper == "2":
                    acl = input("\nACL Name: ")
                    if os.path.isfile(acl):
                        ip = input("\nIP Address: ")
                        del_ip(acl,ip)
                        input("\nPress any key to continue...\n")
                    else:
                        print("ACL NOT FOUND!")
                        input("\nPress any key to continue...\n")
                # exit IP
                elif oper == "3":
                    flag = "1"
                else:
                    print("WRONG OPTION!")
    # read ACL
    elif opt == "2":
        call(['clear'])
        print("\n\n>>>>>>>>>> READ <<<<<<<<<<\n\n")
        acls = glob("*.acl")
        if len(acls) == 0:
            print("NO ACLs WERE FOUND!")
            input("\nPress any key to continue...\n")
        else:
            for f in acls:
                print(f, end="")
            acl = input("\n\nACL Name: ")
            if os.path.isfile(acl):
                read_acl(acl)
                input("\nPress any key to continue...\n")
            else:
                print("ACL NOT FOUND!")
                input("\nPress any key to continue...\n")
    # list ACLs
    elif opt == "3":
        call(['clear'])
        print("\n\n>>>>>>>>>> LIST <<<<<<<<<<\n\n")
        acls = glob("*.acl")
        if len(acls) == 0:
            print("NO ACLs WERE FOUND!")
            input("\nPress any key to continue...\n")
        else:
            for acl in acls:
                print("> ",acl)
                input("\nPress any key to continue...\n")
    # exit...
    elif opt == "4":
        print("\nBye!\n")
        sys.exit(0)
    else:
        print("Wrong Option!")
        input("\nPress any key to continue...\n")

