#!/usr/bin/python3

"""  MongoDB utilities for PyCaptive. """

import bcrypt
from datetime import datetime, timedelta
from pymongo import MongoClient

from app import log

class Connector:
    """ MongoDB connector and jobs: login, add session and delete session. """

    def connect(self):
        """ Preparing MongoDB client. """
        db_user = "mongo"
        db_pass = "mongo"
        db_addr = "127.0.0.1:27017"
        uri = "mongodb://{0}:{1}@{2}".format(db_user,db_pass,db_addr)
        client = MongoClient(uri,serverSelectionTimeoutMS=6000)
        return client


    def add_session(self,username,ipaddress):
        """ Adding login record. """
        client = self.connect()
        db = client.tjs
        collection = db.Sessions
        try:
            login_time = datetime.now()
            # defines the amount of time that a sessions lasts
            expire_time = login_time + timedelta(minutes=2)
            collection.insert_one({"UserName":username,"IpAddress":ipaddress,"LoginTime":login_time,"ExpireTime":expire_time})
            log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "mongodb", "add_session", ipaddress, "OK")
            return 0
        except Exception as e:
            log.error('[%s] %s %s %s', datetime.now(), "EVENT", "mongodb", "add_session:EXCEPTION")
            log.error('%s', e)
            return e


    def expire_sessions(self):
        """  Deleting login record. """
        client = self.connect()
        db = client.tjs
        collection = db.Sessions
        try:
            sessions = collection.find().distinct("ExpireTime")
            deleted_sessions = []
            for session in sessions:
                data = collection.find_one({"ExpireTime":session},{"IpAddress":1,"UserName":1,"_id":0})
                ip = data["IpAddress"]
                if session < datetime.now():
                    collection.delete_one({"ExpireTime":session})
                    #deleted_sessions.append(ip["IpAddress"])
                    deleted_sessions.append(ip)
                    log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "mongodb", "expire_sessions", data, "OK")
            return deleted_sessions
        except Exception as e:
            log.error('[%s] %s %s %s %s', datetime.now(), "EVENT", "mongodb", "expire_sessions", "EXCEPTION")
            log.error('%s', e)
            return e


    def login(self,username,password):   
        """ Validating username and password. """
        client = self.connect()
        db = client.tjs
        collection = db.Users
        try:
            hash_pass = collection.find_one({"UserName":username},{"Password":1,"_id":0})
            if hash_pass is not None:
                hash_pass = hash_pass["Password"]
                unhashed_pass = bcrypt.hashpw(password.encode("utf-8"),hash_pass)
                if hash_pass == unhashed_pass:
                    log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "mongodb", "login", username, "OK")
                    return 0
                else:
                    log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "mongodb", "login", username, "OK")
                    return 2
            else:
                log.error('[%s] %s %s %s %s %s', datetime.now(), "EVENT", "mongodb" ,"login", username, "OK")
                return 1
        except Exception as e:
            log.error('[%s] %s %s %s %s', datetime.now(), "EVENT", "mongodb", "login", "EXCEPTION")
            log.error('%s', e)
            return e
