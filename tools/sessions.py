#!/usr/bin/python3
""" Jobs for session management. """

from datetime import datetime

__author__ == "@ivanleoncz"

import database
import subprocess as sp
import sys


def expire_session(db,username):
    """ Expire session (Database + Firewall). """
    try:
        session = db.Sessions.find_one({"UserName":username})
        if session is not None:
            print("Session: ", session)
            ip = session["IpAddress"]
            oper = input("* Expire (y/n)? ")
            if oper == "y":
                expire  = db.Sessions.delete_one({"UserName":username})
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
    except Exception as e:
        print("ERROR:", e)


def list_sessions(db):
    """ List all active sessions. """
    try:
        sessions = db.Sessions.find({},{"_id":0})
        for session in sessions:
            print(session)
    except Exception as e:
        print("ERROR: ", e)


def helper():
    """ Provides default messages for help purposes. """
    print("\n",sys.argv[0],"\n")
    print("    --list:   list all active sessions")
    print("    --expire: expire sessions based on username")
    print("    --help:   this help")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        helper()
    else:        
        mongo = database.MongoDB()
        db = mongo.connect()
        param = sys.argv[1]
        if param == "--list":
            print("[Sessions]\n")
            list_sessions(db)
        elif param == "--expire":
            username = input("Username: ")
            if username is not None:
                print("[Expire]\n")
                expire_session(db,username)
            else:
                print("INFO: must inform username.")
        else:
            helper() 
