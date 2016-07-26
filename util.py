# coding=utf-8
import json
from datetime import datetime, timedelta
from dbdetails import dbdetails
from random import randint
import socket
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

br = "<br>"

country_list = OrderedDict([
    ('_??', "Desconocido"),
    ('_eu', "Europa"),
    ('de', "Alemania"),
    ('es', "España"),
    ('can', "Islas Canarias"),
    ('can_foreigners', "Extranjeros en Canarias"),
    ('ne', "Países Bajos"),
    ('gb', "Gran Bretaña"),
    ('it', "Italia"),
    ('fr', "Francia"),
    ('no', "Noruega"),
    ('poland', "Poland"),
    ('sweden', "Suecia"),
    ('switzerland', "Suiza"),
    ('austria', "Austria"),
    ('belgium', "Belgia"),
    ('_asia', "Asia"),
    ('china', "China"),
    ('japan', "Japan"),
    ('korea', "Korea"),
    ('india', "India"),
    ('_america', "America"),
    ('us', "EE.UU."),
    ('_southamerica', "Sur-America"),
    ('_africa', "África"),
    ('_xx', "Otro")
])

def print_header(t="text/html"):
    print "Content-Type: "+ t + ";charset=utf-8"
    print

def println(*lns):
    for ln in lns:
        print ln
    print "<br>"

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

def calc_purchases_totals(ps):
    cash_total = 0
    card_total = 0
    for pk, p in enumerate(ps):
        ps[pk]['purchase']['total'] = 0
        for ik, item in enumerate(p['cart']):
            ps[pk]['purchase']['total'] += item['price'] * item['quantity']
            if p['purchase']['card']:
                card_total += item['price'] * item['quantity']
            else:
                cash_total += item['price'] * item['quantity']
    return ps, card_total, cash_total

def uniqueId(*args):
    return randint(100000000, 999999999)

def checkConnection(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print ex.message
    return False

def datestring(date):
    try:
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except AttributeError as e:
        if str(e) == "'unicode' object has no attribute 'strftime'":
            return date
        else:
            raise

def stringdate(string):
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

# Jinja Filters:
def dateformat(value):
    return value.strftime('%Y-%m-%d')

def datetimeformat(value):
    return value.strftime('%Y-%m-%d %H:%M')

def timeformat(value):
    return value.strftime('%H:%M')

def moneyformat(value):
    extrazero = "0" if value % 10 == 0 else ""
    return str((value / 100.0)) + extrazero + "&nbsp;€"

def countryformat(value):
    return country_list[value]

def cardformat(value):
    return "VISA" if value else ""

def discountformat(value):
    return "(-" + str(value) + "%) " if value > 0 else ""

def adddays(date, summand):
    return date + timedelta(days=summand)
# Jinja Tests:
def is_continent(value):
    return value[0] == "_"
def is_today(value):
    return is_same_day(datetime.now(), value)
