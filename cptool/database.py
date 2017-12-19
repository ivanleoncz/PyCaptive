#!/usr/bin/python3

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
                        insert = db.Authentication.insert_one(user_data)
                print("\nDone!\n")
            else:
                print("\nFile not found: ", self.imp)
        except Exception as e:
            print("Exception!", e)
            print(" - line:", line)


    def export_users(self):
        print("\n[Exporting]\n")
        try:
            if os.path.isfile(self.exp):
                db = self.connect()
                query = db.Authentication.find({},{"_id":0})
                if query.count() > 0:
                    with open (self.exp,"a") as f:
                        for user in query:
                            f.write(str(user) + "\n")
                    print("\nDone!\n")
                else:
                    print("\nNo users were found!\n")
            else:
                print("File not found: ", self.exp)
        except Exception as e:
            print("Exception!", e)


    def expire_session(self):
        print("\n[Expire Session]\n")
        try:
            db = self.connect()
            sessions = db.AuthenticationTempRecords.find({},{"_id":0})
            print("> Sessions")
            for session in sessions:
                print(session)
            username = input("\n* Username: ")            
            query = db.AuthenticationTempRecords.find_one({"UserName":username})
            if query is not None:
                find_session = db.AuthenticationTempRecords.find_one({"UserName":username})
                ip = find_session["IpAddress"]
                if find_session is not None:
                    loop = 0
                    while loop == 0:
                        oper = input("* Expire Session (y/n)? ")
                        if oper == "y":
                            loop = 1
                            expire = db.AuthenticationTempRecords.delete_one({"UserName":username})
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
    print("\nA module, not a script! \n\nUse cptool.py: python3 cptool.py\n")

