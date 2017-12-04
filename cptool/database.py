#!/usr/bin/python3

from pymongo import MongoClient

class MongoDB:

    def connect(self):
        db_user = "mongo"
        db_pass = "mongo"
        db_addr = "127.0.0.1:27017"
        uri = "mongodb://{0}:{1}@{2}".format(db_user,db_pass,db_addr)
        client = MongoClient(uri,serverSelectionTimeoutMS=6000)
        db = client.tjs
        return db

if __name__ == "__main__":
    print("\nA module, not a script! \n\nUse cptool.py: python3 cptool.py\n")

