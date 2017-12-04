#!/usr/bin/python3

import bcrypt
from datetime import datetime
from getpass import getpass

import database

mongo = database.MongoDB()
db = mongo.connect()

class Users:

    def validate_pass(self,salt):
        loop = 0
        while loop == 0:
            password = getpass(prompt="* Password: ").encode('utf-8')
            password2 = getpass(prompt="* Retype:   ").encode('utf-8')
            if password == password2:
                loop = 1
                passhash = bcrypt.hashpw(password, salt)
                return passhash
            else:
                print("\n!!! Passwords are not the same !!! Try again!")


    def check_credentials(self,username):
        print("\n\n[Checking Credentials] ->",username,"\n")
        try:
            query = db.Authentication.find_one({"Usuario":username},{"Clave":1,"_id":0})
            if query is not None:
                salt_db = query["Clave"]
                salt_pass = self.validate_pass(salt_db)
                if salt_pass == salt_db:
                    print("\nCorrect!\n")
                else:
                    print("\nWrong Password!\n")
            else:
                print("Username/Password Not Found!")
        except (Exception,KeyboardInterrupt) as e:
            print("\nInterrupted! ", e)

    # must be validated...
    def find_users(self,search):
        query = db.Authentication.find(
            {"$or": 
                [
                    {"Usuario":{"$regex":search+".*"}},
                    {"Nombre":{"$regex":search+".*"}}
                ]
            }, {"Usuario":1,"_id":0}
        )
        return query


    def create(self):
        try:
            print("\n\n[Creating User]\n")
            salt = bcrypt.gensalt()
            user_data = {}
            user_data["Nombre"]    = input("* Nombre:    ")
            user_data["Area"]      = input("* Area:      ")
            user_data["Ocupación"] = input("* Ocupación: ")
            user_data["Correo"]    = input("* Correo:    ")
            user_data["Usuario"]   = input("* Usuario:   ")
            user_data["Clave"]     = self.validate_pass(salt)
            user_data["Creación"]     = datetime.now()
            user_data["Modificación"] = datetime.now()
            print("========================================\n")
            print("* Nombre:    [",user_data["Nombre"],"]")
            print("* Area:      [",user_data["Area"],"]")
            print("* Ocupación: [",user_data["Ocupación"],"]")
            print("* Correo:    [",user_data["Correo"],"]")
            print("* Usuario:   [",user_data["Usuario"],"]")
            print("* Clave:     [",user_data["Clave"],"]")
            loop = 0
            while loop == 0:
                ans = input("\nConfirm (y/n)? ")
                if ans == "y":
                    loop = 1
                    insert = db.Authentication.insert_one(user_data)
                    if insert is not None:
                        print("Done!")
                        self.check_credentials(user_data["Usuario"])
                    else:
                        print("Fail to process query!")
                elif ans == "n":
                    loop = 1
                    print("Aborted!")
                else:
                    input("Wrong option! Press any key...")
        except (Exception,KeyboardInterrupt) as e:
            print("\nInterrupted! ", e)


    def remove(self):
        try:
            print("\n\n[Removing User]\n")
            user = input("Search: ")
            # query = find_users(user)
            query = db.Authentication.find({"$or": [
                                                       {"Usuario":{"$regex":user+".*"}},
                                                       {"Nombre":{"$regex":user+".*"}}
                                                    ] 
                                            },{"Usuario":1,"_id":0})
            for user in query:
                print("*", user["Usuario"])
            usr = input("\nInsert the username: ")
            remove = db.Authentication.delete_one({"Usuario":usr})
            if remove is not None:
                print("Done!")
            else:
                print("Fail to process query!")
        except Exception as e:
            print("\nInterrupted! ", e)

    def update(self):
        try:
            print("\n\n[Update User]\n")
            user = input("Search: ")
            query = find_users(user)
            for usr in query:
                print("*", user["Usuario"])



if __name__ == "__main__":
    print("\nA module, not a script! \n\nUse cptool.py: python3 cptool.py\n")

