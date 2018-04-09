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
    password  = getpass(prompt="\n* Password: ").encode('utf-8')
    password2 = getpass(prompt="* Retype:   ").encode('utf-8')
    if password == password2:
        pass_hash = bcrypt.hashpw(password, salt)
        return pass_hash
    else:
        return "NOT_EQUAL"           


def check_credentials(username):
    """ Verifies if the credentials are valid. """
    query = db.Users.find_one({"UserName":username}, {"Password":1, "_id":0})
    if query is not None:
        pass_db = query["Password"]
        pass_hash = password_hash(pass_db)
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
    if s_type == "full":
        print("\n[Search Full]")
        query = db.Users.find(
            {"$or": 
                [
                    {"UserName":{"$regex":username+".*"}},
                    {"FullName":{"$regex":username+".*"}}
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
    elif s_type == "summary":
        print("\n[Search]")
        query = db.Users.find(
            {"$or": 
                [
                    {"UserName":{"$regex":username+".*"}},
                    {"FullName":{"$regex":username+".*"}}
                ]
            }, {"UserName":1,"_id":0}
        )
        if query.count() > 0:
            users = []
            for usr in query:
                users.append(usr["UserName"])
            return "- %s" % ", ".join(users)


def create(username):
    """ Creates a user. """
    salt = bcrypt.gensalt()
    data = {}
    data["FullName"]     = input("* Nombre:    ")
    data["Area"]         = input("* Area:      ")
    data["Role"]         = input("* Ocupación: ")
    data["Email"]        = input("* Correo:    ")
    data["UserName"]     = username
    data["Password"]     = password_hash(salt)
    data["Creation"]     = datetime.now()
    data["Modification"] = datetime.now()
    print("\n----------------------------------------------\n")
    print("- Nombre:    [",data["FullName"],"]")
    print("- Area:      [",data["Area"],"]")
    print("- Ocupación: [",data["Role"],"]")
    print("- Correo:    [",data["Email"],"]")
    print("- Usuario:   [",data["UserName"],"]")
    ans = input("\nConfirm (y/n)? ")
    if ans == "y":
        db.Users.insert_one(data)
        print("Done!\n")
    elif ans == "n":
        print("Aborted!\n")
    else:
        input("Wrong option! Press any key...")


def remove(username):
    """ Removes a user. """
    print("\n[Remove]")
    user = db.Users.find_one({"UserName":username})
    if user is not None:
        oper = input("Confirm deletion (y/n)?")
        if oper == "y":
            data = db.Users.delete_one({"UserName":username})
            return "Done!"
        else:
            return "Aborted!"
    else:
        return "User Not Found!"


def update(username):
    """ Updates user information. """
    user_data = db.Users.find_one({"UserName":username})
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
                    {"$set":{"UserName":up_username, "Modification":ts}})
                print("\nDone!\n")
        elif opt == "5":
            salt = bcrypt.gensalt()
            up_password = password_hash(salt)
            if up_password is not "NOT_EQUAL":
                db.Users.update_one(
                    {"UserName":username},
                    {"$set":{"Password":up_password, "Modification":ts}})
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
        username = input("\n* Username: ")
        if username is not None:
            if param == "--credentials":
                print("\n[Checking Credentials]")
                check_credentials(username)
            elif param == "--search":
                print(search(username, "summary"))
            elif param == "--search-full":
                search(username, "full")
            elif param == "--create":
                print("\n[Create]")
                create(username)
            elif param == "--remove":
                print(remove(username))
            elif param == "--update":
                print("\n[Update]")
                update(username)
            else:
                helper() 
