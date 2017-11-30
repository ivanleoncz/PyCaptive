#!/usr/bin/python3

import bcrypt
from bson import json_util
from datetime import datetime
from getpass import getpass
import json
from pymongo import MongoClient
import sys

def connect():
    db_user = "mongo"
    db_pass = "mongo"
    db_addr = "127.0.0.1:27017"
    uri = "mongodb://{0}:{1}@{2}".format(db_user,db_pass,db_addr)
    client = MongoClient(uri,serverSelectionTimeoutMS=6000)
    return client

def db_collection():
    client = connect()
    db = client.tjs
    collection = db.Authentication
    return collection

def hashpass(salt):
    loop = 0
    while loop == 0:
        password = getpass(prompt="\n* Password: ").encode('utf-8')
        password2 = getpass(prompt="* Retype:   ").encode('utf-8')
        if password == password2:
           loop = 1
           passhash = bcrypt.hashpw(password, salt)
           return passhash
        else:
           print("\n!!! Passwords are not the same !!! Try again!")


def check_credentials(username):
    print("\n[Checking Credentials]")
    print("\nusername ->", username)
    try:
        query = db_collection().find_one({"Username":username},{"Password":1,"_id":0})
        if query is not None:
            salt_pass = query["Password"]
            unhash_pass = hashpass(salt_pass)
            if unhash_pass == salt_pass:
                return "\nCorrect!\n"
            else:
                return "\nWrong Password!\n"    
        else:
            return "Username/Password Not Found!"
    except (Exception,KeyboardInterrupt) as e:
        return "\nInterrupted!"


def create_user():
    try:
        print("\n[Creating User]\n")
        salt = bcrypt.gensalt()
        user_data = {}
        user_data["Name"]         = input("* Full Name:  ")
        user_data["Sector"]       = input("* Sector:     ")
        user_data["Email"]        = input("* Email:      ")
        user_data["Username"]     = input("* Username:   ")
        user_data["Password"]     = hashpass(salt)
        user_data["Creation"]     = datetime.now()
        user_data["Modification"] = datetime.now()
        print("========================================\n")
        print("* Full Name: [",user_data["Name"],"]")
        print("* Email:     [",user_data["Email"],"]")
        print("* Username:  [",user_data["Username"],"]")
        print("* Sector:    [",user_data["Sector"],"]")
        print("* Password:  [",user_data["Password"],"]")
        loop = 0
        while loop == 0:
            ans = input("\nConfirm (y/n)? ")
            if ans == "y":
                loop = 1
                db_collection().insert_one(user_data)
                print("Done!")
            elif ans == "n":
                loop = 1
                print("Bye!")
            else:
                input("Wrong option! Press any key...")

    except Exception as e:
        print("\nInterrupted! ", e)

result = check_credentials("ivanleoncz")
print(result)
