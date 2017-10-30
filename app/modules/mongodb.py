#!/usr/bin/python3

"""  MongoDB utilities for PyCaptive. """

import bcrypt
from datetime import datetime,timedelta
from pymongo import MongoClient

class Connector:
    """ MongoDB connector. """
    client = None

    def connect(self):
        """ Preparing Client """
        db_user = "mongo"
        db_pass = "mongo"
        uri = "mongodb://{0}:{1}@127.0.0.1:27017".format(db_user,db_pass)
        self.client = MongoClient(uri,serverSelectionTimeoutMS=6000)

    def add_record(self,username,ipaddress):
        """ Adding Login Record """
        self.connect()
        db = self.client.tjs
        collection = db.AuthenticationTempRecords
        try:
            login_time = datetime.now()
            expire_time = login_time + timedelta(minutes=2)
            collection.insert_one({"Username":username,"IpAddress":ipaddress,"LoginTime":login_time,"ExpireTime":expire_time})
            return 0
        except Exception as e:
            return "ERROR: %s" % e

    def del_records(self):
        """  Deleting Login Record """
        self.connect()
        db = self.client.tjs
        collection = db.AuthenticationTempRecords
        try:
            sessions = collection.find().distinct("ExpireTime")
            deleted_sessions = []
            for session in sessions:
                ip = collection.find_one({"ExpireTime":session},{"IpAddress":1,"_id":0})
                if session < datetime.now():
                    collection.delete_one({"ExpireTime":session})
                    deleted_sessions.append(ip["IpAddress"])
            return deleted_sessions
        except Exception as e:
            return "ERROR: %s" % e
            
    def login(self,username,password):   
        """ Connecting to MongoDB, validating username/password. """
        try:
            self.connect()
            db = self.client.tjs
            collection = db.Authentication
            hash_pass = collection.find_one({"Username":username},{"Password":1,"_id":0})
            if hash_pass:
                hash_pass = hash_pass["Password"].encode("utf-8")
                unhashed_pass = bcrypt.hashpw(password.encode('utf-8'),hash_pass)
                if hash_pass == unhashed_pass:
                    return 0
                else:
                    return 2
            else:
                return 1
        except Exception as e:
            return "ERROR: %s" % e
