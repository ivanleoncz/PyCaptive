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
            query = db.Authentication.find_one({"UserName":username},{"Password":1,"_id":0})
            if query is not None:
                salt_db = query["Password"]
                salt_pass = self.validate_pass(salt_db)
                if salt_pass == salt_db:
                    print("\nCorrect!\n")
                else:
                    print("\nWrong Password!\n")
            else:
                print("UserName/Password Not Found!")
        except (Exception,KeyboardInterrupt) as e:
            print("\nInterrupted! ", e)


    def find_users(self,search,opt):
        if opt == "full":
            query = db.Authentication.find(
                {"$or": 
                    [
                        {"UserName":{"$regex":search+".*"}},
                        {"FullName":{"$regex":search+".*"}}
                    ]
                    }, {"Password":0,"_id":0}
            )
            return query
        elif opt == "username":
            query = db.Authentication.find(
                {"$or": 
                    [
                        {"UserName":{"$regex":search+".*"}},
                        {"FullName":{"$regex":search+".*"}}
                    ]
                }, {"UserName":1,"_id":0}
            )
            return query



    def create(self):
        try:
            print("\n\n[Creating User]\n")
            salt = bcrypt.gensalt()
            user_data = {}
            user_data["FullName"]     = input("* Nombre:    ")
            user_data["Area"]         = input("* Area:      ")
            user_data["Role"]         = input("* Ocupación: ")
            user_data["Email"]        = input("* Correo:    ")
            user_data["UserName"]     = input("* Usuario:   ")
            user_data["Password"]     = self.validate_pass(salt)
            user_data["Creation"]     = datetime.now()
            user_data["Modification"] = datetime.now()
            print("========================================\n")
            print("* Nombre:    [",user_data["Name"],"]")
            print("* Area:      [",user_data["Area"],"]")
            print("* Ocupación: [",user_data["Role"],"]")
            print("* Correo:    [",user_data["Email"],"]")
            print("* Usuario:   [",user_data["UserName"],"]")
            print("* Clave:     [",user_data["Password"],"]")
            loop = 0
            while loop == 0:
                ans = input("\nConfirm (y/n)? ")
                if ans == "y":
                    loop = 1
                    insert = db.Authentication.insert_one(user_data)
                    if insert is not None:
                        print("Done!")
                        self.check_credentials(user_data["UserName"])
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
            query = self.find_users(user,"username")
            for user in query:
                print("*", user["UserName"])
            user = input("\nInsert the username: ")
            remove = db.Authentication.delete_one({"UserName":user})
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
            query = self.find_users(user,"full")
            for usr in query:
                print("\n----------------------------------------------")
                print("* Nombre        : ",usr["Name"])
                print("* Area          : ",usr["Area"])
                print("* Ocupación     : ",usr["Role"])
                print("* Correo        : ",usr["Email"])
                print("* Usuario       : ",usr["UserName"])
                print("* Creación      : ",usr["Creation"])
                print("* Actualización : ",usr["Modification"])
            user = input("Username: ")
            query = db.Authentication.find_one({"UserName": user})
            for usr in query:
                nombre  = usr["Name"]
                area    = usr["Area"]
                role    = usr["Role"]
                correo  = usr["Email"]
                usuario = usr["UserName"]
            print("\n1. Nombre\n2. Area\n3. Ocupación\n4. Correo\n5. Usuario ")
            opt = input("Opción (ex.: 5) ? ")
            if opt == "1":
                query = db.Authentication.find_one({"FullName":})
            elif opt == "2":
            elif opt == "3":
            elif opt == "4":
            elif opt == "5":


                query = db.Authentication.update_one({'Usuario':user},{'$set':{'Usuario':user}})
                if query is not None:
                    print("")
                    query = db.Authetication.find_one({'Usuario':user},{"Password":0,"_id":0})
                    if query is not None:
                        print("\n----------------------------------------------")
                        print("* Nombre        : ",usr["Name"])
                        print("* Area          : ",usr["Area"])
                        print("* Ocupación     : ",usr["Role"])
                        print("* Correo        : ",usr["Email"])
                        print("* Usuario       : ",usr["UserName"])
                        print("* Creación      : ",usr["Creation"])
                        print("* Actualización : ",usr["Modification"])
                    
        except (Exception,KeyboardInterrupt) as e:
            print("\nInterrupted! ", e)


if __name__ == "__main__":
    print("\nA module, not a script! \n\nUse cptool.py: python3 cptool.py\n")

