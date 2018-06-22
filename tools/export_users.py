#!/usr/bin/python3
""" Exporting users from MongoDB database. """

__author__ = "@ivanleoncz"

import database
import subprocess as sp
import sys


def export_users(csv):
    """ Export users from .csv file. """
    print("INFO: do not import this file !!!***")
    mongo = database.MongoDB()
    db = mongo.connect()
    try:
        users = db.Users.find({},{"_id":0})
        if users.count() > 0:
            with open (csv, "w") as f:
                for user in users:
                    f.write("*** DO NOT IMPORT THIS FILE ***\n")
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


def helper():
    """ Provides default messages for help purposes. """
    print(sys.argv[0],"\n")
    print("    --export: export users to .csv file (file cannot be used for import)")
    print("    --help:   this help")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        helper()
    else:
        param = sys.argv[1]
        if param == "--export":
            print("[Exporting]\n")
            export_users("pycaptive_users_export.out")
        else:
            helper() 
