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

def calc_daily_total(ps):
    cash_total = 0
    card_total = 0
    for p in ps:
         (syncId, status, country, card, discount, date) = p['purchase']
         if not is_same_day(date, datetime.now()):
             continue
         for item in p['cart']:
            (title, status, boxId, quantity, price) = item
            if card:
                card_total += price * quantity
            else:
                cash_total  += price * quantity
    daily_total = cash_total + card_total
    return (daily_total, cash_total, card_total)

def print_purchases(ps, shown_date):
    print "<ul>"
    daily_total_str = [str(total / 100.0) + "€" for total in calc_daily_total(ps)]
    print '<li>Total: ', daily_total_str[0], '</li>'
    print '<li>Cash-Total: ', daily_total_str[1], '</li>'
    print '<li>Card-Total: ', daily_total_str[2], '</li>'
    for p in ps:
        (syncId, status, country, card, discount, date) = p['purchase']
        if not is_same_day(date, shown_date):
            continue
        card_str = "with card" if card else "in cash"
        disc_str = "" if discount == 0 else " and got " + str(discount) + "% off"
        total = 0
        for item in p['cart']:
            (title, status, boxId, quantity, price) = item
            total += price*quantity
        date_str = date.strftime('%H:%M')
        delete_link = '<a href="api.py?action=delete_purchase&redirect=index.py&syncId=' + str(syncId) + '">borrar</a>'
        print "<li>", date_str, " from ", country, " paid ", (total / 100.0), "€ ", card_str, disc_str, delete_link, "</li>"
        print "<ul>"
        for item in p['cart']:
            (title, status, boxId, quantity, price) = item
            print "<li>", quantity, "x ", title, " at ", (price / 100.0), "€</li>"
        print "</ul>"
    print "</ul>"

def print_date_form(date):
    now = date.strftime('%Y-%m-%d')
    print '<form action="" method="post">'
    print '<input type="text" name="date" value="' + now + '">'
    print '<input type="submit">'
    print '</form>'

def is_same_day(date1, date2):
    return datetime.strftime(date1, '%Y-%m-%d') == datetime.strftime(date2, '%Y-%m-%d')

css = ("ul            { list-style-type: none; }"
       "ul#details    { padding: 10; }"
       "ul#details li { display: inline; margin-left: 10px; }"
       "#details      { top: 0; width: 100%; margin: 0; background: white; }"
       ".hidden       { visibility: hidden; }"
       ".fixed        { position: fixed; }"
      )
base = CgBase()
util.print_header()
util.print_html_header("Herramiento", css)
purchases = base.get_purchases()
date = form.getfirst('date')
if date is None:
    date = datetime.now()
else:
    date = datetime.strptime(date, '%Y-%m-%d')
print_date_form(date)
print '<h2>Compras de hoy</h2>'
print_purchases(purchases, date)
util.print_html_footer()
