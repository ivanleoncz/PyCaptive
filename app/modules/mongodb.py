"""  MongoDB client configuration and actions. """

from app import log
from datetime import datetime, timedelta
from pymongo import MongoClient

__author__ = "@ivanleoncz"

import bcrypt

class Connector:
    """ MongoDB setup and actions. """

    def connect(self):
        """ Preparing MongoDB client. """
        db_user = "mongo"
        db_pass = "mongo"
        db_addr = "127.0.0.1:27017"
        uri = "mongodb://{0}:{1}@{2}".format(db_user, db_pass, db_addr)
        client = MongoClient(uri, serverSelectionTimeoutMS=6000)
        return client


    def add_session(self, username, client_ip, user_data):
        """ Adding session. """
        client = self.connect()
        db = client.tjs
        collection = db.Sessions
        login_time = datetime.now()
        expire_time = login_time + timedelta(hours=12)
        try:
            collection.insert_one({
                "UserName":username,
                "IpAddress":client_ip,
                "OS":user_data.get("os"),
                "Browser":user_data.get("browser"),
                "Device":user_data.get("device"),
                "Brand":user_data.get("brand"),
                "Family":user_data.get("family"),
                "LoginTime":login_time,
                "ExpireTime":expire_time})
            log.error('[%s] %s %s %s %s %s %s',
              login_time, "mongodb", "add_session", "OK",
              username, client_ip, user_data)
            return 0
        except Exception as e:
            log.error('[%s] %s %s %s',
                       login_time, "mongodb", "add_session", "EXCEPTION")
            log.error('%s', e)
            return e


    def check_session(self, username, ipaddress):
        """ Checking existence of session, returning session data. """
        client = self.connect()
        db = client.tjs
        collection = db.Sessions
        session_data = collection.find_one(
                {"IpAddress":ipaddress},
                {"UserName":1, "IpAddress":1, "_id":0})
        if session_data:
            return session_data
        else:
            return False


    def expire_sessions(self):
        """  Expires session. """
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
                    log.error('[%s] %s %s %s %s',
                            time_now, "mongodb", "expire_sessions", data, "OK")
            return deleted_sessions
        except Exception as e:
            log.error('[%s] %s %s %s',
                       time_now, "mongodb", "expire_sessions", "EXCEPTION")
            log.error('%s', e)
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
                    log.error('[%s] %s %s %s %s',
                               ts, "mongodb", "login", username, "OK")
                    return 0
                else:
                    log.error('[%s] %s %s %s %s',
                               ts, "mongodb", "login", username, "NOK")
                    return 2
            else:
                log.error('[%s] %s %s %s %s',
                           ts, "mongodb" ,"login", username, "NOK")
                return 1
        except Exception as e:
            log.error('[%s] %s %s %s',
                       ts, "mongodb", "login", "EXCEPTION")
            log.error('%s', e)
            return e
