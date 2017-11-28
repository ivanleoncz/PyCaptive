#!/usr/bin/python3

import json
from bson import json_util
from pymongo import MongoClient

def connect():
    db_user = "mongo"
    db_pass = "mongo"
    db_addr = "127.0.0.1:27017"
    uri = "mongodb://{0}:{1}@{2}".format(db_user,db_pass,db_addr)
    client = MongoClient(uri,serverSelectionTimeoutMS=6000)
    return client

client = connect()
db = client.tjs
collection = db.Authentication

username = collection.find_one({"Username":"ivan.leon"})
data = json.dumps(username, indent=4, default=json_util.default)
print(data)
