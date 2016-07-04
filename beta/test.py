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


br = "<br>"
base = CgBase()
util.print_header()
util.print_html_header("Test")

purchases = base.get_purchases(getDeleted=True, prettydict=True)
#base.cur.execute("ALTER TABLE purchases ADD edited DATETIME NOT NULL AFTER  status")
#base.cur.execute("ALTER TABLE cart ADD edited DATETIME NOT NULL AFTER status")
for p in purchases:
    syncId = p['purchase']['syncId']
    date = p['purchase']['date']
    print syncId, date, br
    print base.update("purchases", {"edited": date}, False, "WHERE syncId = " + str(syncId))
    for item in p['cart']:
        boxId = item['boxId']
        print base.update("cart", {"edited": date}, False, "WHERE syncId = " + str(syncId) + " AND boxId = " + str(boxId))
        print item, br
    print br, br
base.db.commit()

util.print_html_footer()
