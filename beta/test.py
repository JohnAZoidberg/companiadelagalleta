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

#print base.update("purchases", {"status": 0}, True, "WHERE status = 3")
#print base.cur.rowcount
db = MySQLdb.connect(host=dbdetails.host,
                             user=dbdetails.user,
                             passwd=dbdetails.passwd,
                             db="backup",
                             use_unicode=True,
                             charset='utf8')
cur = db.cursor()
cur.execute("SELECT date FROM purchases GROUP BY date having count(*) >= 2")
ps = cur.fetchall()
for p in ps:
    print p, util.br
