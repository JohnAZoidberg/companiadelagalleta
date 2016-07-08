#!/usr/bin/python -u
# coding=utf-8
import cgitb
cgitb.enable()
import cgi
import json
from datetime import datetime
from dbconn import *
from random import randint
import requests
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import util
import subprocess
form = cgi.FieldStorage()


def shellUpdate():
    subprocess.call("./update.sh")

version = 0
base = CgBase()
try:
    base.cur.execute("SELECT version FROM config")
    result = base.cur.fetchone()
    version = result[0]
except Exception as e:
    if str(e) == "(1146, \"Table 'cg.config' doesn't exist\")":
        version = 0 # 0.0.0
    else:
        raise

response = requests.get().json()
serverVersion = reponse['version']

if serverVersion > version:
    shellUpdate()
print "Location update.py"
print 
