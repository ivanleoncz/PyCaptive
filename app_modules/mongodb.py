#!/usr/bin/python3

from pymongo import MongoClient
""" MongoDB connector and tools for PyCaptive.  """

class Connector:

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

    def login(self):
        """ Connecting and looking for username/password"""
        self.connect()
        try:
            db = self.client["tjs"]
            col = db["Authentication"]
            doc = col.find_one({"Username":self.username,"Password":self.password})
            if doc:
                return "ok"
            else:
                return "nok"
        except Exception as e:
            print("Exception:",e)
            return "db timeout"

 
