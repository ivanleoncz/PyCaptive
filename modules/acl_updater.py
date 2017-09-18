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
            print("Line: ",line)
    return "DONE!"

while True:
    call(['clear'])
    print("\n\n-------------------------------")
    print("--------- ACL UPDATER ---------")
    print("-------------------------------")
    print("1. Modify ACL")
    print("2. Read ACL")
    print("3. List ACLs")
    print("4. Exit")
    opt = input("\n> ")
    # modify ACL
    if opt == "1":
        flag = "0"
        while flag == "0":
            print("\n\n---------- MODIFY ---------")
            print("1. Add IP")
            print("2. Del IP")
            print("3. Exit")
            oper = input("\n> ")
            if oper == "1":
                acl = input("ACL Name: ")
                if os.path.isfile(acl):
                    ip = input("IP Address: ")
                    add_ip(f,acl)
                    print("\nDone!")
                else:
                    print("\nACL NOT FOUND!")
                    input("Press any key to continue...")
            elif oper == "2":
                acl = input("\nFile Name: ")
                if os.path.isfile(acl):
                    ip = input("\nIP Address: ")
                    del_ip(acl,ip)
                    print("\nDone!")
                else:
                    print("\nACL NOT FOUND!")
                    input("Press any key to continue...")
            elif oper == "3":
                flag = "1"
            else:
                print("\nWRONG OPTION!")
    # read ACL
    elif opt == "2":
        print("\n\n---------- READ -----------")
        acl = input("\nFile Name: ")
        if os.path.isfile(acl):
            read_acl(acl)
            print("\nDone!")
        else:
            print("\nACL NOT FOUND!")
            input("Press any key to continue...")
    # list ACLs
    elif opt == "3":
        print("\n\n---------- LIST -----------")
        acls = glob("*.acl")
        if len(acls) != 0:
            for acl in acls:
                print("\n> ",acl)
        else:
            print("\nNO ACLs WERE FOUND!")
            input("Press any key to continue...")
    # wrong option
    elif opt == "4":
        print("Bye!")
        sys.exit(0)
    else:
        print("\nWRONG OPTION!")

