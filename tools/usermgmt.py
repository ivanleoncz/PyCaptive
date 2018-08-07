#!/usr/bin/python3
""" Create, Read, Update and Delete users from PyCaptive database. """

from datetime import datetime
from getpass import getpass

__author__ = "@ivanleoncz"

import bcrypt
import database
import subprocess as sp
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
    """ Verifies if credentials are valid. """
    print("\n[Checking Credentials]")
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
    """ Presents user info (full or summary). """
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
    print("\n[Create]")
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
    print("\n[Update]")
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


def expire_session(username):
    """ Expire session (Database + Firewall). """
    session = db.Sessions.find_one({"UserName":username})
    if session is not None:
        print("Session: ", session)
        ip = session["IpAddress"]
        oper = input("* Expire (y/n)? ")
        if oper == "y":
            expire  = db.Sessions.delete_many({"UserName":username})
            binary  = "/sbin/iptables"
            table   = "mangle"
            chain   = "PREROUTING"
            nic     = "eth2"
            jump    = "INTERNET"
            command = [binary, '-t', table, '-D', chain, '-i', nic,
                                  '-s', ip, '-j', jump]
            result = sp.call(command)
            if result == 0:
                print("INFO: Done!\n")
            else:
                print("ERROR: Fail to remove IPTABLES/Netfilter rule.\n")
        else:
            print("INFO: Bye!")
    else:
        print("INFO: Session Not Found!")


def list_sessions(username=None):
    """ List all active sessions. """
    print("[Sessions]")
    sessions = None
    if username is None:
        sessions = db.Sessions.find({}, {"_id":0})
    else:
        sessions = db.Sessions.find({"UserName":{"$regex":username+".*"}},
                                                               {"_id":0})
    for session in sessions:
        print("->", session)


def helper():
    """ Provides help. """
    print(sys.argv[0],"\n")
    print("    --search:       searches user and returns info (summary)")
    print("    --search-full:  searches user and returns info (full)")
    print("    --credentials:  verifies user credentials")
    print("    --update:       updates information for a user")
    print("    --create:       creates user")
    print("    --remove:       removes user")
    print("    --expire:       expire session for a user")
    print("    --sessions:     list active sessions")
    print("    --help:         this help")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        helper()
    else:
        mongo = database.MongoDB()
        db = mongo.connect()
        param = sys.argv[1]
        if param == "--credentials":
            username = input("\n* Username: ")
            check_credentials(username)
        elif param == "--search":
            username = input("\n* Username: ")
            print(search(username, "summary"))
        elif param == "--search-full":
            username = input("\n* Username: ")
            search(username, "full")
        elif param == "--create":
            username = input("\n* Username: ")
            create(username)
        elif param == "--remove":
            username = input("\n* Username: ")
            print(remove(username))
        elif param == "--update":
            username = input("\n* Username: ")
            update(username)
        elif param == "--expire":
            username = input("\n* Username: ")
            expire_session(username)
        elif param == "--sessions":
            username = input("\n* Username: ")
            if username is '':
                list_sessions()
            else:
                list_sessions(username)
        elif param == "--help":
            helper()
        else:
            helper()
