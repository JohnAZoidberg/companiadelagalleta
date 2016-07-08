#!/usr/bin/python -u
# coding=utf-8
import cgitb
cgitb.enable()
import cgi
import json
from datetime import datetime
from dbconn import *
from random import randint
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import util
import subprocess

def git_update():
    return subprocess.check_output("./update.sh")

def db_update():
    base = CgBase()
    new_version = 116 # 0.1.16
    version = 0
    try:
        base.cur.execute("SELECT version FROM config")
        result = base.cur.fetchone()
        version = result[0]
    except Exception as e:
        if str(e) == "(1146, \"Table 'cg.config' doesn't exist\")":
            version = 0 # 0.0.0
    if version < 10: # 0.1.0
        carts = base.fetchall("cart", ["syncId"], "")
        purchases = base.fetchall("purchases", ["syncId"], "") 
        for cart in carts:
            if cart not in purchases:
                print cart, (cart in purchases), util.br
                sql = "DELETE FROM cart WHERE syncId=" + str(cart[0])
                base.cur.execute(sql)
        base.cur.execute("DELETE FROM cart WHERE syncId=482836353 AND boxId=17 LIMIT 1")
        try:
            base.cur.execute("ALTER TABLE cart DROP COLUMN edited")
        except:
           pass
        try:
            base.cur.execute("ALTER TABLE cart DROP COLUMN status")
        except:
           pass
        try:
            base.cur.execute("DROP TABLE config")
        except:
            pass
        base.db.commit()
        try:
            sql = (
                  "CREATE TABLE config ("
                  "constant CHAR(1) DEFAULT 'X' NOT NULL PRIMARY KEY,"
                  "CHECK (constant = 'X'),"
                  "version int DEFAULT 10 NOT NULL,"
                  "last_sync datetime DEFAULT '2016-01-01 00:00:00' NOT NULL"
                  ")"
                  )
            base.cur.execute(sql)
            base.cur.execute("INSERT INTO config () VALUES ()")
        except:
            base.db.rollback()
            raise
        base.insert("boxes", {"title": "Basic bag pequeña - GRATIS", "price": 0, "boxesEntryId": 65}, False)
        base.db.commit()
    if version < 12:
        print "This version does not add anything new :P", util.br
    if new_version is not None:
        base.update("config", {"version": new_version}, True, "WHERE constant = 'X'")
    if version != new_version:
        print "Updated to version: " + str(new_version)
    else:
        print "No update available"
