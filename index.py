#!/usr/bin/python -u
# coding=utf-8
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


def print_form():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print '<form action="api.py" method="post">'
    print '<input type="hidden" name="redirect" value="index.py">'
    print '<input type="hidden" name="action" value="save_purchase">'
    print '<ul style="list-style-type: none;">'
    for key, cookie in util.cookie_list.iteritems():
        print '<li><label>'
        print '<input type="number" name="box_' + str(key) + '" value="0" size="2" required>'
        print cookie
        print '</label></li>'
    print '<li><select name="country">'
    for key, country in util.country_list.iteritems():
        print '<option value="' + str(key) + '">' + country + '</option>'
    print '</select></li>'
    print '<li><label>Date: <input type="text" name="datetime" value="'+now+'" placeholder="'+now+'"></label></li>'
    print '<li><label>Discount: <input type="text" name="discount" value="0" size="2" required>%</label></li>'
    print '<li><label>Tarjeta? <input type="checkbox" name="tarjeta"></label></li>'
    print '<li><input type="submit" value="Save"></li>'
    print '</ul>'
    print '</form>'

def print_purchases(ps):
    print "<ul>"
    for key, p in ps.iteritems():
        (country, card, discount, date) = p['purchase']
        card_str = "with card" if card else "in cash"
        disc_str = "" if discount == 0 else " and got " + str(discount) + "% off"
        total = 0
        for item in p['cart']:
            (title, boxId, quantity, price) = item
            total += price*quantity
        print "<li>", date, " from ", country, " paid ", (total / 100.0), "€ ", card_str, disc_str, "</li>"
        print "<ul>"
        for item in p['cart']:
            (title, boxId, quantity, price) = item
            print "<li>", quantity, "x ", title, " at ", (price / 100.0), "€</li>"
        print "</ul>"
    print "</ul>"

base = CgBase()
util.print_header()
util.print_html_header("Herramiento")
purchases = base.get_purchases()
#util.println('<a href="analysis.py">Analyze</a>')
print_form()
print '<hr>'
print_purchases(purchases)
util.print_html_footer()
