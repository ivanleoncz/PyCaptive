#!/usr/bin/python3

import bcrypt
from datetime import datetime
from getpass import getpass
import database

mongo = database.MongoDB()
db = mongo.connect()

class Users:
    
    def password_hash(self,salt):
        password  = getpass(prompt="* Password: ").encode('utf-8')
        password2 = getpass(prompt="* Retype:   ").encode('utf-8')
        if password == password2:
            pass_hash = bcrypt.hashpw(password, salt)
            return pass_hash
        else:
            return "NOT_EQUAL"           


    def check_credentials(self):
        try:
            print("\n\n[Checking Credentials]\n")
            username = input("* Username: ")
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
                print("\nUserName: Not Found\n")
        except (Exception,KeyboardInterrupt) as e:
            print("\nInterrupted! ", e)


    def search(self,data):
        print("\n\n[Searching Users]\n")
        search_user = input("* Name or Username: ")
        if data == "full":
            query = db.Users.find(
                {"$or": 
                    [
                        {"UserName":{"$regex":search_user+".*"}},
                        {"FullName":{"$regex":search_user+".*"}}
                    ]
                    }, {"Password":0,"_id":0}
            )
            if query.count() > 0:
                for usr in query:       # presenting users that were found
                    print("\n----------------------------------------------\n")
                    print("- Nombre        : ",usr["FullName"])
                    print("- Area          : ",usr["Area"])
                    print("- Ocupación     : ",usr["Role"])
                    print("- Correo        : ",usr["Email"])
                    print("- Usuario       : ",usr["UserName"])
                    print("- Creación      : ",usr["Creation"])
                    print("- Actualización : ",usr["Modification"])
                return "OK"
            else:
                return "NOK"
        elif data == "normal":
            query = db.Users.find(
                {"$or": 
                    [
                        {"UserName":{"$regex":search_user+".*"}},
                        {"FullName":{"$regex":search_user+".*"}}
                    ]
                }, {"UserName":1,"_id":0}
            )
            if query.count() > 0:
                for usr in query:       # presenting users that were found (just UserName)
                    print("- ", usr["UserName"])
                return "OK"
            else:
                return "NOK"
        else:
            print("Wrong Option!")


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
            user_data["Password"]     = self.password_hash(salt)
            user_data["Creation"]     = datetime.now()
            user_data["Modification"] = datetime.now()
            print("\n----------------------------------------------\n")
            print("- Nombre:    [",user_data["FullName"],"]")
            print("- Area:      [",user_data["Area"],"]")
            print("- Ocupación: [",user_data["Role"],"]")
            print("- Correo:    [",user_data["Email"],"]")
            print("- Usuario:   [",user_data["UserName"],"]")
            loop = 0
            while loop == 0:
                ans = input("\nConfirm (y/n)? ")
                if ans == "y":
                    loop = 1
                    db.Users.insert_one(user_data)
                    print("\nDone!\n")
                elif ans == "n":
                    loop = 1
                    print("\nAborted!\n")
                else:
                    input("Wrong option! Press any key...")
        except (Exception,KeyboardInterrupt) as e:
            print("\nInterrupted! ", e)


    def remove(self):
        try:
            self.search("normal")
            print("\n\n[Removing User]\n")
            user = input("* Username: ")
            data = db.Users.delete_one({"UserName":user})
            print("\nDone!\n")
        except Exception as e:
            print("\nInterrupted! ", e)


    def update(self):
        try: 
            users = self.search("full")    # find all users that have FullName or UserName similar
            print("\n\n[Update User]\n")
            if users == "OK" :
                user = input("* Username: ")
                user_data = db.Users.find_one({"UserName": user})    # find a specific user from the list above
                if user_data is not None: 
                    area      = user_data["Area"]           # extracting values of the query
                    ocupación = user_data["Role"]           # extracting values of the query
                    correo    = user_data["Email"]          # extracting values of the query
                    usuario   = user_data["UserName"]       # extracting values of the query
                    loop = 0
                    while loop == 0:
                        print("\n1. Area\n2. Ocupación\n3. Correo\n4. Usuario\n5. Clave\n\n")
                        opt = input("> ")
                        if opt == "1":
                            loop = 1
                            up_area = input("* Area: ")
                            if up_area is not "":
                                db.Users.update_one({"Area":area},{"$set":{"Area":up_area,"Modification":datetime.now()}})
                                print("\nDone!\n")
                        elif opt == "2":
                            loop = 1
                            up_role = input("* Ocupación: ")
                            if up_role is not "":
                                db.Users.update_one({"Role":ocupación},{"$set":{"Role":up_role,"Modification":datetime.now()}})
                                print("\nDone!\n")
                        elif opt == "3":
                            loop = 1
                            up_email = input("* Correo: ")
                            if up_email is not "":
                                db.Users.update_one({"Email":correo},{"$set":{"Email":up_email,"Modification":datetime.now()}})
                                print("\nDone!\n")
                        elif opt == "4":
                            loop = 1
                            up_username = input("* Usuario: ")
                            if up_username is not "":
                                db.Users.update_one({"UserName":usuario},{"$set":{"UserName":up_username,"Modification":datetime.now()}})
                                print("\nDone!\n")
                        elif opt == "5":
                            loop = 1
                            salt = bcrypt.gensalt()
                            up_password = self.password_hash(salt)
                            if up_password is not "NOT_EQUAL":
                                # got to make sure that there isn't two users with the same username
                                db.Users.update_one({"UserName":usuario},{"$set":{"Password":up_password,"Modification":datetime.now()}})
                                print("\nDone!\n")
                        else:
                            print("\nWrong Option!\n")
                else:
                    print("\nUser Not Found!\n")
            else:
                print("\nUser/Users Not Found!\n")
        except (Exception,KeyboardInterrupt) as e:
            print("\nInterrupted! ", e)


if __name__ == "__main__":
    print("\nCannot be imported!\n\nRun: sudo ./pycap_tool.py\n")

