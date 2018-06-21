#!/usr/bin/python3
""" Importing users to MongoDB database. """

from datetime import datetime

__author__ = "@ivanleoncz"

import bcrypt
import database
import os
import subprocess as sp
import sys


def import_users(file_db): 
    """ Importing users from .csv file. """
    mongo = database.MongoDB()
    db = mongo.connect()
    try:
        with open(file_db,"r") as f:
            print("Format expected:\n")
            print("John, Adm, Analyst, john@foobar.com, john, 5up3r")
            print("Alan, Oper, Analyst, alan@foobar.com, alan, s3cr3t")
            opt = input("\nConfirm Import (y/n)? ")
            if opt == "y":
                for line in f:
                    print("Processing line:", line)
                    user_data = {}
                    salt = bcrypt.gensalt()
                    timestamp = datetime.now()
                    line_split = line.split(',')
                    user_data["FullName"]     = line_split[0]
                    user_data["Area"]         = line_split[1]
                    user_data["Role"]         = line_split[2]
                    user_data["Email"]        = line_split[3]
                    user_data["UserName"]     = line_split[4]
                    p_text                 = line_split[5].rstrip('\n')
                    p_hash = bcrypt.hashpw(p_text.encode('utf8'),salt)
                    user_data["Password"]     = p_hash
                    user_data["Creation"]     = timestamp
                    user_data["Modification"] = timestamp
                    insert = db.Users.insert_one(user_data)
                print("Done!")
            else:
                print("Bye!")
    except Exception as e:
        print("Exception!", e)
        print(" - line:", line)


def helper():
    """ Provides default messages for help purposes. """
    print(sys.argv[0],"\n")
    print("    --import: import users from .csv file")
    print("    --help:   this help")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        helper()
    else:
        param = sys.argv[1]
        if param == "--import":
            print("[Importing]\n")
            import_users("pycaptive_users.csv")
        else:
            helper() 
