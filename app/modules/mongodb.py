"""  MongoDB client configuration and actions. """

from datetime import datetime, timedelta

from pymongo import MongoClient

from app import log, DB_URI, SESSION_DURATION

__author__ = "@ivanleoncz"

import bcrypt

class Connector:
    """ MongoDB setup and actions. """

    def connect(self):
        """ Preparing MongoDB client. """
        client = MongoClient(DB_URI, serverSelectionTimeoutMS=6000)
        return client


    def add_session(self, username, client_ip, user_data):
        """ Adding session. """
        client = self.connect()
        db = client.tjs
        collection = db.Sessions
        login_time = datetime.now()
        expire_time = login_time + timedelta(hours=SESSION_DURATION)
        try:
            collection.insert_one({
                "UserName":username,
                "IpAddress":client_ip,
                "UserData":user_data,
                "LoginTime":login_time,
                "ExpireTime":expire_time})
            log.info('%s %s %s %s %s %s', "mongodb", "add_session", "OK",
                                           username, client_ip, user_data)
            return 0
        except Exception as e:
            log.critical('%s %s %s', "mongodb", "add_session", "EXCEPTION")
            log.critical('%s', e)
            return e


    def check_session(self, username, ipaddress):
        """ Check session session data and returns it. """
        client = self.connect()
        db = client.tjs
        collection = db.Sessions
        session_data = collection.find_one( {"IpAddress":ipaddress} )
        if session_data:
            return session_data
        else:
            return False


    def expire_sessions(self):
        """ Expires sessions. """
        client = self.connect()
        db = client.tjs
        collection = db.Sessions
        time_now = datetime.now()
        try:
            sessions = collection.find().distinct("ExpireTime")
            deleted_sessions = []
            for session in sessions:
                data = collection.find_one(
                        {"ExpireTime":session},
                        {"IpAddress":1, "UserName":1, "_id":0})
                ip = data["IpAddress"]
                if session < time_now:
                    collection.delete_one({"ExpireTime":session})
                    deleted_sessions.append(ip)
                    log.info('%s %s %s %s',
                             "mongodb", "expire_sessions", "OK", data)
            return deleted_sessions
        except Exception as e:
            log.critical('%s %s %s', "mongodb", "expire_sessions", "EXCEPTION")
            log.critical('%s', e)
            return e


    def login(self, username, password):
        """ Validating username and password for login. """
        client = self.connect()
        db = client.tjs
        collection = db.Users
        ts = datetime.now()
        try:
            hash_pass = collection.find_one({"UserName":username},
                                            {"Password":1, "_id":0})
            if hash_pass is not None:
                db_hash = hash_pass["Password"]
                new_hash = bcrypt.hashpw(password.encode("utf-8"), db_hash)
                if db_hash == new_hash:
                    log.info('%s %s %s %s', "mongodb", "login", "OK, "username)
                    return 0
                else:
                    log.error('%s %s %s %s %s',
                              "mongodb", "login", "NOK", username, "WRONG_PASS")
                    return 2
            else:
                log.error('%s %s %s %s %s',
                          "mongodb" ,"login", "NOK", username, "NOT_FOUND")
                return 1
        except Exception as e:
            log.critical('%s %s %s %s',
                         "mongodb", "login", "EXCEPTION", username)
            log.critical('%s', e)
            return e
