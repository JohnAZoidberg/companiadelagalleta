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
form = cgi.FieldStorage()

base = CgBase()
util.print_header()
new_version = None
try:
    base.cur.execute("SELECT version FROM config")
    result = base.cur.fetchone()
    version = result[0]
except Exception as e:
    if str(e) == "(1146, \"Table 'cg.config' doesn't exist\")":
        version = 0 # 0.0.0
if version < 10: # 0.1.0
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
    base.db.commit()
    new_version = 10
if new_version is not None:
    print "Updated to version: " + str(new_version)
else:
    print "No update"
