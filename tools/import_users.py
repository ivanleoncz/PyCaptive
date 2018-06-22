#!/usr/bin/python3
""" Importing users to MongoDB database. """

from datetime import datetime

__author__ = "@ivanleoncz"

import bcrypt
import database
import os
import subprocess as sp
import sys


def import_users(csv): 
    """ Importing users from .csv file. """
    mongo = database.MongoDB()
    db = mongo.connect()
    try:
        with open(csv, "r") as f:
            print("Format expected:\n")
            print("John, Adm, Analyst, john@foobar.com, john, 5up3r")
            print("Alan, Oper, Analyst, alan@foobar.com, alan, s3cr3t")
            opt = input("\nConfirm Import (y/n)? ")
            if opt == "y":
                for line in f:
                    line_split = line.split(',')
                    print("INFO: processing user ->", line_split[4])
                    user_data = {}
                    salt = bcrypt.gensalt()
                    timestamp = datetime.now()
                    user_data["FullName"]     = line_split[0]
                    user_data["Area"]         = line_split[1]
                    user_data["Role"]         = line_split[2]
                    user_data["Email"]        = line_split[3]
                    user_data["UserName"]     = line_split[4]
                    p_text                    = line_split[5].rstrip('\n')
                    p_hash = bcrypt.hashpw(p_text.encode('utf8'), salt)
                    user_data["Password"]     = p_hash
                    user_data["Creation"]     = timestamp
                    user_data["Modification"] = timestamp
                    insert = db.Users.insert_one(user_data)
                print("Done!")
            else:
                print("Bye!")
    except Exception as e:
        print("ERROR:", e)
        print(" - line:", line)


csv = "pycaptive_users.csv"
if os.path.isfile(csv):
    import_users(csv)
else:
    print("ERROR: file not found -> ", csv)
