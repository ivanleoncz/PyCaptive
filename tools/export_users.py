#!/usr/bin/python3
""" Exporting users from MongoDB database. """

__author__ = "@ivanleoncz"

import database
import subprocess as sp
import sys


def export_users():
    """ Export users from .csv file. """
    mongo = database.MongoDB()
    db = mongo.connect()
    try:
        users = db.Users.find({},{"_id":0})
        if users.count() > 0:
            with open (mongo.exp,"w") as f:
                f.write("\nDON'T USE this format for importing users !\n")
                for user in query:
                    line = "{0},{1},{2},{3},{5}".format(
                            user["FullName"],user["Area"],user["Role"],
                            user["Email"],user["UserName"]
                    )
                    f.write(line + "\n")
                print("Done!")
        else:
            print("No users were found!")
    except Exception as e:
        print("Exception!", e)


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
            export_users()
        else:
            helper() 
