"""  MongoDB client configuration and actions. """

import bcrypt
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from json import dumps
from pymongo import MongoClient
from app import log
from app import mongodb_dict as d

__author__ = "@ivanleoncz"


class Connector:
    """ MongoDB setup and actions. """

    def __init__(self):
        """ Preparing MongoDB client. """
        self.client = MongoClient(d.get("DB_URI"), serverSelectionTimeoutMS=6000)


    def add_session(self, username, client_ip, user_data):
        """ Adding session. """
        db = self.client.pycaptive.Sessions
        login_time = datetime.now()
        expire_time = login_time + timedelta(seconds=d.get("SESSION_DURATION"))
        session_id = None
        try:
            session_id = db.insert({
                "UserName":username,
                "IpAddress":client_ip,
                "UserData":user_data,
                "LoginTime":login_time,
                "ExpireTime":expire_time})
            self.client.close()
            log.info('%s %s %s %s %s %s', "mongodb", "add_session", "OK",
                                           username, client_ip, user_data)
            return session_id
        except Exception as e:
            log.critical('%s %s %s', "mongodb", "add_session", "EXCEPTION")
            log.critical('%s', e)
            return e


    def check_session(self, session_id):
        """
        Check existence of a session, based on ObjectID.

        Parameters
        ----------
        session_id : string
            MongoDB ObjectID from add_session() (see /login route).

        Return
        ------
            Session data (see add_session()).
        """
        db = self.client.pycaptive.Sessions
        data = db.find_one({"_id":ObjectId(session_id)})
        self.client.close()
        if data:
            return data
        else:
            return False


    def dump_sessions(self):
        db = self.client.pycaptive.Sessions
        data = db.find({})
        data = [record for record in data]
        self.client.close()
        if data:
            return dumps(data, indent=2, default=json_util.default)
        else:
            return False


    def expire_sessions(self):
        """ Expires sessions. """
        db = self.client.pycaptive.Sessions
        time_now = datetime.now()
        expired_sessions = []
        try:
            sessions = db.find().distinct("ExpireTime")
            for session in sessions:
                data = db.find_one(
                        {"ExpireTime":session},
                        {"IpAddress":1, "UserName":1, "_id":0})
                ip = data["IpAddress"]
                if session < time_now:
                    db.delete_one({"ExpireTime":session})
                    expired_sessions.append(ip)
                    log.info('%s %s %s %s',
                             "mongodb", "expire_sessions", "OK", data)
            self.client.close()
            return expired_sessions
        except Exception as e:
            log.critical('%s %s %s', "mongodb", "expire_sessions", "EXCEPTION")
            log.critical('%s', e)
            return e


    def login(self, username, password):
        """ Validating username and password for login. """
        db = self.client.pycaptive.Users
        ts = datetime.now()
        try:
            hash_pass = db.find_one({"UserName":username},
                                    {"Password":1, "_id":0})
            self.client.close()
            if hash_pass is not None:
                db_hash = hash_pass["Password"]
                new_hash = bcrypt.hashpw(password.encode("utf-8"), db_hash)
                if db_hash == new_hash:
                    log.info('%s %s %s %s', "mongodb", "login", "OK", username)
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
