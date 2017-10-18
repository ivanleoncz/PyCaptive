#!/usr/bin/python3

"""  MongoDB utilities for PyCaptive.

     Return Codes:

     0x0000 - Successful
     0x0db1 - Fail To Execute Query
     0x0db2 - User Not Found
     0x0db3 - Wrong Password
     0x0db4 - Fail To Add Record
     0x0db5 - Fail To Del Record
"""

import bcrypt
from datetime import datetime,timedelta
from pymongo import MongoClient

class Connector:
    """ MongoDB connector. """
    db = None
    client = None
    username = None
    ipaddress = None

    def connect(self):
        """ Preparing Client. """
        db_user = "mongo"
        db_pass = "mongo"
        uri = "mongodb://{0}:{1}@127.0.0.1:27017".format(db_user,db_pass)
        self.client = MongoClient(uri,serverSelectionTimeoutMS=6000)

    def login_record(self,oper):
        """ Login Record Tasks. """
        collection = self.db.AuthenticationTempRecords
        if oper == "add":
            try:
                login_time = datetime.now()
                expire_time = login_time + timedelta(hours=3)
                collection.insert_one({"Username":self.username,"IpAddress":self.ipaddress"LoginTime":login_time,"ExpireTime":expire_time})
                return "0x0000"
            except Exception as e:
                return "0x0db4"
        elif oper == "del":
            try:
                time_now = datetime.now()
                time_now = str(time_now).split(".")[0]
                expired_sessions = collection.find().distinct("ExpireTime")
                for session in expired_sessions:
                    if session < time_now:
                        collection.delete_one({"Username":self.username})    
                return "0x0000"
            except Exception as e:
                return "0x0db5"
        else:
            return "Wrong Option!"
            
    def login(self,username,password,ipaddress):   
        """ Connecting to MongoDB, validating username/password + other functions. """
        self.username = username
        self.ipaddress = ipaddress
        try:
            self.connect()
            self.db = self.client.tjs
            collection = self.db.Authentication
            hash_pass = collection.find_one({"Username":self.username},{"Password":1,"_id":0})
            if hash_pass:
                hash_pass = hash_pass["Password"].encode("utf-8")
                unhashed_pass = bcrypt.hashpw(password.encode('utf-8'),hash_pass)
                if hash_pass == unhashed_pass:
                    record = self.login_record("add")
                    if record == "0x0000":
                        return "0x0000"
                    else:
                        return "0x0db4"
                else:
                    return "0x0db3"
            else:
                return "0x0db2"
        except Exception as e:
            return "0x0db1"

