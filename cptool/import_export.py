#!/usr/bin/python3

import bcrypt
from datetime import datetime
import os
import sys

import database

mongo = database.MongoDB()
db = mongo.connect()

class Transfer:

    def import_users(self,file_csv):
        print("\n\n[Importing]\n")
        with open(file_csv,"r") as f:
            try:
                for line in f:
                    user_data = {}
                    timestamp = datetime.now()
                    line_split = line.split(',')
                    user_data["FullName"] = line_split[0] 
                    user_data["Area"] = line_split[1]
                    user_data["Role"] = line_split[2]
                    user_data["Email"] = line_split[3]
                    user_data["UserName"] = line_split[4]
                    salt = bcrypt.gensalt()
                    # Exception! Unicode-objects must be encoded before hashing 
                    passhash = bcrypt.hashpw(line_split[5].rstrip('\n'),salt)
                    user_data["Password"] = passhash
                    user_data["Creation"] = timestamp
                    user_data["Modification"] = timestamp
                    insert = db.Authentication.insert_one(user_data)
            except Exception as e:
                print("Exception!", e) 
                print(" - line:", line)


    def export_users(self,file_csv):
        print("\n\n[Exporting]\n")
        query = db.Authentication.find({},{"_id":0})
        if query is not None:
            with open (file_csv,"a") as f:
                for user in query:
                    f.write(str(user) + "\n")
            print("Done!")
        else:
            print("Fail to process query!")


if __name__ == "__main__":
    print("\nA module, not a script! \n\nUse cptool.py: python3 cptool.py\n")

