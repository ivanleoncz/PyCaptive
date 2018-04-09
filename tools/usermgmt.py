#!/usr/bin/python3
""" Create, Delete and Update users. """

# TODO: got to make sure that there isn't two users with the same username

from datetime import datetime
from getpass import getpass

__author__ = "@ivanleoncz"

import bcrypt
import database
import sys                                                                              
    
def password_hash(salt):
    """ Returns password hash. """
    password  = getpass(prompt="* Password: ").encode('utf-8')
    password2 = getpass(prompt="* Retype:   ").encode('utf-8')
    if password == password2:
        pass_hash = bcrypt.hashpw(password, salt)
        return pass_hash
    else:
        return "NOT_EQUAL"           


def check_credentials(username):
    """ Verifies if the credentials are valid. """
    query = db.Users.find_one({"UserName":username},{"Password":1,"_id":0})
    if query is not None:
        pass_db = query["Password"]
        pass_hash = self.password_hash(pass_db)
        if pass_db == pass_hash:
            print("\nUserName: OK")
            print("Password: OK\n")
        else:
            print("\nUserName: OK")
            print("Password: NOK\n")    
    else:
        print("ERROR: Username Not Found\n")


def search(username,s_type):
    """ Searches/presents user info (full or summary). """
    if s_type == "full":     # presenting users (full info)
        query = db.Users.find(
            {"$or": 
                [
                    {"UserName":{"$regex":search_user+".*"}},
                    {"FullName":{"$regex":search_user+".*"}}
                ]
            },  {"Password":0,"_id":0}
        )
        if query.count() > 0:
            for usr in query:
                print("\n----------------------------------------------\n")
                print("- Nombre        : ",usr["FullName"])
                print("- Area          : ",usr["Area"])
                print("- Ocupación     : ",usr["Role"])
                print("- Correo        : ",usr["Email"])
                print("- Usuario       : ",usr["UserName"])
                print("- Creación      : ",usr["Creation"])
                print("- Actualización : ",usr["Modification"])
    elif s_type == "summary":    # presenting users (summary info)
        query = db.Users.find(
            {"$or": 
                [
                    {"UserName":{"$regex":search_user+".*"}},
                    {"FullName":{"$regex":search_user+".*"}}
                ]
            }, {"UserName":1,"_id":0}
        )
        if query.count() > 0:
            for usr in query:
                print("- ", usr["UserName"])


def create(username):
    """ Creates a user. """
    salt = bcrypt.gensalt()
    user_data = {}
    user_data["FullName"]     = input("* Nombre:    ")
    user_data["Area"]         = input("* Area:      ")
    user_data["Role"]         = input("* Ocupación: ")
    user_data["Email"]        = input("* Correo:    ")
    user_data["UserName"]     = input("* Usuario:   ")
    user_data["Password"]     = self.password_hash(salt)
    user_data["Creation"]     = datetime.now()
    user_data["Modification"] = datetime.now()
    print("\n----------------------------------------------\n")
    print("- Nombre:    [",user_data["FullName"],"]")
    print("- Area:      [",user_data["Area"],"]")
    print("- Ocupación: [",user_data["Role"],"]")
    print("- Correo:    [",user_data["Email"],"]")
    print("- Usuario:   [",user_data["UserName"],"]")
    ans = input("\nConfirm (y/n)? ")
    if ans == "y":
        db.Users.insert_one(user_data)
        print("Done!\n")
    elif ans == "n":
        print("Aborted!\n")
    else:
        input("Wrong option! Press any key...")


def remove(username):
    """ Removes a user. """
    data = db.Users.delete_one({"UserName":username})
    return "Done!"


def update(username):
    """ Updates user information. """
    user_data = db.Users.find_one({"UserName": username})
    if user_data is not None: 
        area      = user_data["Area"]
        role      = user_data["Role"]
        email     = user_data["Email"]
        username  = user_data["UserName"]
        ts        = datetime.now()
        print("\n1. Area\n2. Role\n3. Email\n4. User\n5. Password\n\n")
        opt = input("> ")
        if opt == "1":
            up_area = input("* Area: ")
            if up_area is not "":
                db.Users.update_one(
                    {"Area":area},
                    {"$set":{"Area":up_area, "Modification":ts}})
                print("\nDone!\n")
        elif opt == "2":
            up_role = input("* Role: ")
            if up_role is not None:
                db.Users.update_one(
                    {"Role":role},
                    {"$set":{"Role":up_role, "Modification":ts}})
                print("\nDone!\n")
        elif opt == "3":
            up_email = input("* Email: ")
            if up_email is not None:
                db.Users.update_one(
                    {"Email":email},
                    {"$set":{"Email":up_email, "Modification":ts}})
                print("\nDone!\n")
        elif opt == "4":
            up_username = input("* Username: ")
            if up_username is not None:
                db.Users.update_one(
                    {"UserName":username},
                    {"$set":{"UserName":up_username,"Modification":ts}})
                print("\nDone!\n")
        elif opt == "5":
            salt = bcrypt.gensalt()
            up_password = self.password_hash(salt)
            if up_password is not "NOT_EQUAL":
                db.Users.update_one(
                    {"UserName":username},
                    {"$set":{"Password":up_password,"Modification":ts}})
            print("\nDone!\n")
        else:
            print("\nWrong Option!\n")
    else:
        print("\nUser/Users Not Found!\n")


def helper():
    """ Provides default messages for help purposes. """
    print(sys.argv[0],"\n")
    print("    --search:       searches user and returns info (summary)")
    print("    --search-full:  searches user and returns info (full)")
    print("    --credentials:  verifies user credentials")
    print("    --update:       updates information for a user")
    print("    --create:       creates user")
    print("    --remove:       removes user")
    print("    --help:         this help")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        helper()
    else:
        mongo = database.MongoDB()
        db = mongo.connect()
        param = sys.argv[1]
        username = input("* Username: ")
        if username is not None:
            if param == "--credentials":
                print("[Checking Credentials]\n")
                check_credentials(username)
            elif param == "--search":
                print("[Search]\n")
                search(username,"summary")
            elif param == "--search-full":
                print("[Search Full]\n")
                search(username,"full")
            elif param == "--create":
                print("[Create]\n")
                create(username)
            elif param == "--remove":
                print("[Remove]\n")
                remove(username)
            elif param == "--update":
                print("[Update]\n")
                update(username)
            else:
                helper() 
