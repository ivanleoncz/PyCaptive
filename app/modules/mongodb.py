#!/usr/bin/python3
"""  MongoDB client configuration and actions. 

After successful login, a session (add_session()) is added to MongoDB,
with and "expire_time" variable defined for N minutes.

The expired sessions are expired via APScheduler, which calculates if
the "ExpireTime" returned via a query, are lower than the current time.

If they are, the sesssions are expired from MongoDB.
"""

from app import log
from datetime import datetime, timedelta
from pymongo import MongoClient

__author__ = "@ivanleoncz"

import bcrypt

class Connector:
    """ MongoDB jobs. """

    def connect(self):
        """ Preparing MongoDB client. """
        db_user = "mongo"
        db_pass = "mongo"
        db_addr = "127.0.0.1:27017"
        uri = "mongodb://{0}:{1}@{2}".format(db_user, db_pass, db_addr)
        client = MongoClient(uri, serverSelectionTimeoutMS=6000)
        return client


    def add_session(self, username, ipaddress):
        """ Adding session record. """
        client = self.connect()
        db = client.tjs
        collection = db.Sessions
        login_time = datetime.now()
        try:
            # defines the amount of time that a sessions lasts
            expire_time = login_time + timedelta(hours=12)
            collection.insert_one({
                "UserName":username,
                "IpAddress":ipaddress,
                "LoginTime":login_time,
                "ExpireTime":expire_time})
            log.error('[%s] %s %s %s %s',
                       login_time, "mongodb", "add_session", ipaddress, "OK")
            return 0
        except Exception as e:
            log.error('[%s] %s %s %s',
                       login_time, "mongodb", "add_session", "EXCEPTION")
            log.error('%s', e)
            return e


    def expire_sessions(self):
        """  Deleting session record. """
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
        """ Validating username and password. """
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
