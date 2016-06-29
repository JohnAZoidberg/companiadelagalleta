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
now_date = datetime.now()
now = now_date.strftime('%Y-%m-%d %H:%M')

def print_form_header(hidden):
    attr = 'id="details"'
    attr += ' class="hidden"'  if hidden else 'class="fixed"'
    print '<ul ' + attr + '>'
    if hidden:
        print "Menu"
    else:
        print '<li>País: <select name="country">'
        for key, country in util.country_list.iteritems():
            print '<option value="' + str(key) + '">' + country + '</option>'
        print '</select></li>'
        print '<li><label title="' + now + '">Date: <input type="text" name="datetime" placeholder="11:45" required></label></li>'
        print '<li><label>Discount: <input type="text" name="discount" value="0" size="2" required>%</label></li>'
        print '<li><label>Tarjeta? <input type="checkbox" name="tarjeta"></label></li>'
        print '<li><input type="submit" value="Save"></li>'
        if not dbdetails.server:
            print '<li><a href="api.py?action=sync&redirect=index.py">Sync con nube</a></li>'
        else:
            print '<li><a href="report.py">Excel</a></li>'
    print '</ul>'

def print_form(boxes):
    print '<form action="api.py" method="post">'
    print '<input type="hidden" name="redirect" value="index.py">'
    print '<input type="hidden" name="action" value="save_purchase">'
    print_form_header(True)
    print_form_header(False)
    print '<ul style="list-style-type: none;">'
    for key, cookie in boxes.iteritems():
        print '<li><label>'
        print '<input type="number" name="box_' + str(key) + '" value="0" size="2" required>'
        print cookie
        print '</label></li>'
    print '</ul>'
    print '</form>'

base = CgBase()
util.print_header()
util.print_html_header("Herramiento", util.css)
purchases = base.get_purchases()
#util.println('<a href="analysis.py">Analyze</a>')
print_form(base.get_boxes())
print '<hr>'
print '<h2>Compras de hoy</h2>'
util.print_purchases(purchases, now_date, "index.py")
util.print_html_footer()
