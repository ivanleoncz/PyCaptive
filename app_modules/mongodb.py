#!/usr/bin/python3
"""  MongoDB utilities for PyCaptive."""

import bcrypt
from datetime import datetime,timedelta
from pymongo import MongoClient

class Connector:
    """ MongoDB connector.  """

    db_user = "mongo"
    db_pass = "mongo"

    client = None
    username = None
    password = None

    def __init__(self,username,password):
        """ Storing username and password from Flask (POST)."""
        self.username = username
        self.password = password

    def connect(self):
        """ Preparing MongoDB connector. """
        uri = "mongodb://{0}:{1}@127.0.0.1:27017".format(self.db_user,self.db_pass)
        self.client = MongoClient(uri,serverSelectionTimeoutMS=6000)

    def login_record(self,db):
        """ Recording successful login attempts. """
        col = db["AuthenticationTempRecords"]
        login = datetime.now()
        expire_time = login + timedelta(hours=3)
        login = str(login).split(".")[0]
        expire_time = str(expire_time).split(".")[0]
        insert_record = col.insert_one({"Username":self.username,"IpAddress":self.ip,"LoginTime":login,"ExpireTime":expiretime})
        if insert_record:
            return "ok"
        else:
            return "nok"

    def login(self):
        """ Connecting and searching for correct username and password.

        0 - Login Ok!
        1 - Wrong Password!
        2 - User Not Found!
        """
        self.connect()
        try:
            db = self.client["tjs"]
            col = db["Authentication"]
            hash_pass = col.find_one({"Username":self.username},{"Password":1,"_id":0})
            if hash_pass:
                hash_pass = hash_pass["Password"].encode("utf-8")
                unhashed_pass = bcrypt.hashpw(self.password.encode('utf-8'),hash_pass)
                if hash_pass == unhashed_pass:
                    # firewall rule must apply here (or not ???...)
                    record = login_record()
                    if record == "ok":
                        return 0
                    else:
                        return 200
                else:
                    return 1
            else:
                return 2
        except Exception as e:
            print("Exception:",e)
            return "db timeout"

