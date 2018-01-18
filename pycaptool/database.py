#!/usr/bin/python3

import bcrypt
from datetime import datetime
import os
import subprocess as sp
from pymongo import MongoClient

class MongoDB:

    imp = "import.csv"
    exp = "export.csv"

    def connect(self):
        db_user = "mongo"
        db_pass = "mongo"
        db_addr = "127.0.0.1:27017"
        uri = "mongodb://{0}:{1}@{2}".format(db_user,db_pass,db_addr)
        client = MongoClient(uri,serverSelectionTimeoutMS=6000)
        db = client.tjs
        return db


    def import_users(self): 
        print("\n[Importing]\n")
        try:
            if os.path.isfile(self.imp):
                db = self.connect()
                with open(self.imp,"r") as f:
                    print("Format expected:\n")
                    print("John, Administration, Manager, john@medicalsystems.com, john, p4ssword1")
                    print("Alan, Maintenance, Supervisor, alan@medicalsystems.com, alan, p4ssword2\n")
                    opt = input("Confirm Import (y/n)? ")
                    if opt == "y":
                        for line in f:
                            user_data = {}
                            timestamp = datetime.now()
                            line_split = line.split(',')
                            user_data["FullName"]    = line_split[0]
                            user_data["Area"]        = line_split[1]
                            user_data["Role"]        = line_split[2]
                            user_data["Email"]       = line_split[3]
                            user_data["UserName"]    = line_split[4]
                            salt = bcrypt.gensalt()
                            password_hash = bcrypt.hashpw(line_split[5].rstrip('\n').encode('utf8'),salt)
                            user_data["Password"]     = password_hash
                            user_data["Creation"]     = timestamp
                            user_data["Modification"] = timestamp
                            insert = db.Users.insert_one(user_data)
                        print("\nDone!\n")
                    elif opt == "n":
                        print("\nBye!\n")
                    else:
                        print("\nWrong Option!\n")
            else:
                print("\nFile not found: ", self.imp)
        except Exception as e:
            print("Exception!", e)
            print(" - line:", line)


    def export_users(self):
        print("\n[Exporting]\n")
        try:
            db = self.connect()
            query = db.Users.find({},{"_id":0})
            if query.count() > 0:
                with open (self.exp,"w") as f:
                    f.write("\n!!! Do not use this file/format for import operations.\n\n")
                    for user in query:
                        line = user["FullName"] + "," + user["Area"] + "," + user["Role"] + "," + user["Email"] + "," + user["UserName"]
                        f.write(line + "\n")
                    print("\nDone!\n")
            else:
                print("\nNo users were found!\n")
        except Exception as e:
            print("Exception!", e)


    def expire_session(self):
        print("\n[Expire Session]\n")
        try:
            db = self.connect()
            sessions = db.Sessions.find({},{"_id":0})
            print("> Sessions")
            for session in sessions:
                print(session)
            username = input("\n* Username: ")            
            query = db.Sessions.find_one({"UserName":username})
            if query is not None:
                find_session = db.Sessions.find_one({"UserName":username})
                ip = find_session["IpAddress"]
                if find_session is not None:
                    loop = 0
                    while loop == 0:
                        oper = input("* Expire Session (y/n)? ")
                        if oper == "y":
                            loop = 1
                            expire = db.Sessions.delete_one({"UserName":username})
                            r = sp.call(['/sbin/iptables', '-D', 'INPUT', '-i', 'lo', '-s', ip, '-p', 'tcp', '--dport', '10800', '-j', 'DROP'])
                            print("\nDone!\n")
                        elif oper == "n":
                            loop = 1
                            print("\nBye!\n")
                        else:
                            print("\nWrong Option!\n")
                else:
                    print("\nNo Session Was Found!\n")
            else:
                print("\nUser Does Not Exit!\n")                
        except Exception as e:
            print("Exception!", e)


if __name__ == "__main__":
    print("\nCannot be imported!\n\nRun: sudo ./pycap_tool.py\n")

