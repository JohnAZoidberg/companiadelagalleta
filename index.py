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
now = datetime.now().strftime('%Y-%m-%d %H:%M')

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
    print '</ul>'

def print_form():
    print '<form action="api.py" method="post">'
    print '<input type="hidden" name="redirect" value="index.py">'
    print '<input type="hidden" name="action" value="save_purchase">'
    print_form_header(True)
    print_form_header(False)
    print '<ul style="list-style-type: none;">'
    for key, cookie in util.cookie_list.iteritems():
        print '<li><label>'
        print '<input type="number" name="box_' + str(key) + '" value="0" size="2" required>'
        print cookie
        print '</label></li>'
    print '</ul>'
    print '</form>'

def calc_daily_total(ps):
    cash_total = 0
    card_total = 0
    for p in ps:
         (syncId, country, card, discount, date) = p['purchase']
         if not is_same_day(date, datetime.now()):
             continue
         for item in p['cart']:
            (title, boxId, quantity, price) = item
            if card:
                card_total += price * quantity
            else:
                cash_total  += price * quantity
    daily_total = cash_total + card_total
    return (daily_total, cash_total, card_total)

def print_purchases(ps):
    print "<ul>"
    daily_total_str = [str(total / 100.0) + "€" for total in calc_daily_total(ps)]
    print '<li>Total: ', daily_total_str[0], '</li>'
    print '<li>Cash-Total: ', daily_total_str[1], '</li>'
    print '<li>Card-Total: ', daily_total_str[2], '</li>'
    for p in ps:
        (syncId, country, card, discount, date) = p['purchase']
        if not is_same_day(date, datetime.now()):
            continue
        card_str = "with card" if card else "in cash"
        disc_str = "" if discount == 0 else " and got " + str(discount) + "% off"
        total = 0
        for item in p['cart']:
            (title, boxId, quantity, price) = item
            total += price*quantity
        date_str = date.strftime('%H:%M')
        delete_link = '<a href="api.py?action=delete_purchase&redirect=index.py&syncId=' + str(syncId) + '">borrar</a>'
        print "<li>", date_str, " from ", country, " paid ", (total / 100.0), "€ ", card_str, disc_str, delete_link, "</li>"
        print "<ul>"
        for item in p['cart']:
            (title, boxId, quantity, price) = item
            print "<li>", quantity, "x ", title, " at ", (price / 100.0), "€</li>"
        print "</ul>"
    print "</ul>"

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
#util.println('<a href="analysis.py">Analyze</a>')
print_form()
print '<hr>'
print '<h2>Compras de hoy</h2>'
print_purchases(purchases)
util.print_html_footer()
