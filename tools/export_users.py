#!/usr/bin/python3
""" Exporting users from MongoDB database. """

__author__ = "@ivanleoncz"

import database
import subprocess as sp
import sys


def export_users(csv):
    """ Export users from .csv file. """
    print("[Exporting]\n")
    print("INFO: do not import this file !!!")
    mongo = database.MongoDB()
    db = mongo.connect()
    try:
        users = db.Users.find({},{"_id":0})
        if users.count() > 0:
            with open (csv, "w") as f:
                f.write("*** DO NOT IMPORT THIS FILE ***\n")
                for user in users:
                    line = "{0},{1},{2},{3},{4}".format(
                            user["FullName"],user["Area"],user["Role"],
                            user["Email"],user["UserName"]
                    )
                    f.write(line + "\n")
                print("Done!")
        else:
            print("INFO: no users to export")
    except Exception as e:
        print("ERROR:", e)


export_users("pycaptive_users.export")
