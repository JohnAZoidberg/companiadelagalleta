#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()
import cgi
import json
from datetime import datetime
from dbconn import *
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import util
form = cgi.FieldStorage()

def print_date_form(datestr):
    print '<form action="" method="get">'
    print '<input type="text" name="date" value="' + datestr + '">'
    print '<input type="submit">'
    print '</form>'

base = CgBase()
util.print_header()
util.print_html_header("Herramiento", css=util.css)
purchases = base.get_purchases()
datestr = form.getfirst('date')
if datestr is None:
    date = datetime.now()
    datestr = date.strftime('%Y-%m-%d')
else:
    date = datetime.strptime(datestr, '%Y-%m-%d')
print_date_form(datestr)
print '<h2>Compras de ' + datestr + '</h2>'
util.print_purchases(purchases, date, "stats.py")
util.print_html_footer()
