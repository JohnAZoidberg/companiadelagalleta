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


def print_form():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
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
    print '<li><label>Date: <input type="text" name="datetime" placeholder="'+now+'"></label></li>'
    print '<li><label>Discount: <input type="text" name="discount" value="0" size="2" required>%</label></li>'
    print '<li><label>Tarjeta? <input type="checkbox" name="tarjeta"></label></li>'
    print '<li><input type="submit" value="Save"></li>'
    print '</ul>'
    print '</form>'
def calc_daily_total(ps):
    daily_total = 0
    for key, p in ps.iteritems():
         (country, card, discount, date) = p['purchase']
         if not is_same_day(date, datetime.now()):
             continue
         for item in p['cart']:
            (title, boxId, quantity, price) = item
            daily_total += price*quantity
    return daily_total

def print_purchases(ps):
    print "<ul>"
    daily_total_str = str(calc_daily_total(ps) / 100.0) + "€"
    print '<li>Total: ', daily_total_str, '</li>'
    for key, p in ps.iteritems():
        (country, card, discount, date) = p['purchase']
        if not is_same_day(date, datetime.now()):
            continue
        card_str = "with card" if card else "in cash"
        disc_str = "" if discount == 0 else " and got " + str(discount) + "% off"
        total = 0
        for item in p['cart']:
            (title, boxId, quantity, price) = item
            total += price*quantity
        date_str = date.strftime('%H:%M')
        print "<li>", date_str, " from ", country, " paid ", (total / 100.0), "€ ", card_str, disc_str, "</li>"
        print "<ul>"
        for item in p['cart']:
            (title, boxId, quantity, price) = item
            print "<li>", quantity, "x ", title, " at ", (price / 100.0), "€</li>"
        print "</ul>"
    print "</ul>"

def is_same_day(date1, date2):
    return datetime.strftime(date1, '%Y-%m-%d') == datetime.strftime(date2, '%Y-%m-%d')

def generate_syncid(date):
    return str(randint(100000000, 999999999))

base = CgBase()
util.print_header()
util.print_html_header("Test")
purchases = base.get_purchases()

br = "<br>"
results = base.fetchall("cart", ["syncId", "boxId"])
for result in results:
    (syncId, boxId) = result
    print result, br
    #base.update("cart", {"syncId": syncid}, "WHERE cartId = " + str(cartId + " AND boxId = " + str(boxId)))

util.print_html_footer()
