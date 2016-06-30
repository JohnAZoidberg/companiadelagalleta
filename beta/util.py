# coding=utf-8
import json
from datetime import datetime
from dbdetails import dbdetails
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

country_list = OrderedDict([
    ('??', "Desconocido"),
    ('de', "Alemania"),
    ('es', "España"),
    ('canario', "Islas Canarias"),
    ('ne', "Países Bajos"),
    ('gb', "Gran Bretaña"),
    ('us', "EE.UU."),
    ('it', "Italia"),
    ('fr', "Francia"),
    ('no', "Noruega"),
    ('xx', "Otro")
])

css = ("ul            { list-style-type: none; }"
       "ul#details    { padding: 10; }"
       "ul#details li { display: inline; margin-left: 10px; }"
       "#details      { top: 0; width: 100%; margin: 0; background: white; }"
       ".hidden       { visibility: hidden; }"
       ".fixed        { position: fixed; }"
      )

def print_header(t="text/html"):
    print "Content-Type: "+ t + ";charset=utf-8"
    print


def print_html_header(title, css=None, js=None):
    print '<html>'
    print '<head>'
    print '<meta name="viewport" content="width=device-width, initial-scale=1">'
    print '<title>' + title + '</title>'
    if css is not None:
        print '<style>' + css + '</style>'
    if js is not None:
        print '<script>' + js + '</script>'
    print '</head>'
    print '<body>'


def print_html_footer():
    print '</body>'
    print '</html>'


def println(*lns):
    for ln in lns:
        print ln
    print "<br>"

def calc_daily_total(ps, shown_date):
    cash_total = 0
    card_total = 0
    for p in ps:
         (syncId, status, country, card, discount, date) = p['purchase']
         if not is_same_day(date, shown_date):
             continue
         for item in p['cart']:
            (title, status, boxId, quantity, price) = item
            if card:
                card_total += price * quantity
            else:
                cash_total  += price * quantity
    daily_total = cash_total + card_total
    return (daily_total, cash_total, card_total)

def print_purchases(ps, shown_date, page):
    print "<ul>"
    daily_total_str = [str(total / 100.0) + "€" for total in calc_daily_total(ps, shown_date)]
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
        delete_link = "" if dbdetails.server else '<a href="api.py?action=delete_purchase&redirect=' + page + '&syncId=' + str(syncId) + '">borrar</a>'
        print '<li title="', syncId, '">', date_str, " from ", country, " paid ", (total / 100.0), "€ ", card_str, disc_str, delete_link, "</li>"
        print "<ul>"
        for item in p['cart']:
            (title, status, boxId, quantity, price) = item
            print '<li title="', boxId, '">', quantity, "x ", title, " at ", (price / 100.0), "€</li>"
        print "</ul>"
    print "</ul>"

def is_same_day(date1, date2):
    return datetime.strftime(date1, '%Y-%m-%d') == datetime.strftime(date2, '%Y-%m-%d')

