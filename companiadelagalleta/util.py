# coding=utf-8
from datetime import datetime
from random import randint
import socket
import os
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from functools import wraps

from flask import request, current_app as app

import jinja_filters

br = "<br>"

weekdays = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo"
]

months = [
    None,
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre"
]

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
    ('portugal', "Portugal"),
    ('denmark', "Dinamarca"),
    ('no', "Noruega"),
    ('poland', "Polonia"),
    ('sweden', "Suecia"),
    ('switzerland', "Suiza"),
    ('austria', "Austria"),
    ('belgium', "Belgia"),
    ('_asia', "Asia"),
    ('china', "China"),
    ('japan', "Japón"),
    ('south-korea', "Corea del sur"),
    ('india', "India"),
    ('_america', "America"),
    ('us', "EE.UU."),
    ('_southamerica', "Sur-America"),
    ('_africa', "África"),
    ('_xx', "Otro")
])

workers = OrderedDict([
    #(0, "Daniel"),
    (1, "Patricia"),
    # (2, "Raquel"),
    (3, "Roberta"),
    # (4, "Paola"),
    (5, "Pedro")
])

all_workers = OrderedDict([
    (0, "Daniel"),
    (1, "Patricia"),
    (2, "Raquel"),
    (3, "Roberta"),
    (4, "Paola"),
    (5, "Pedro")
])

locations = OrderedDict([
    (0, "Meloneras"),
    (1, "Obrador"),
    (2, "Las Palmas"),
    (3, "Puerto de la Cruz")
])

containers = {
    1: {"boxes": [1], "title": "Carta 10"},
    2: {"boxes": [2, 63], "title": "Carta 20"},
    3: {"boxes": [3], "title": "Carta 30"},
    4: {"boxes": [5, 6, 7, 8, 65, 66], "title": "Basic bag pequeña"},
    5: {"boxes": [10, 11, 12, 13, 57], "title": "Basic bag grande"},
    6: {"boxes": [15, 16, 17, 18, 58], "title": "Cube pequeño"},
    7: {"boxes": [20, 21, 22, 23, 59], "title": "Cube grande"},
    8: {"boxes": [25, 26, 27, 28], "title": "Pyramid"},
    9: {"boxes": [30, 31, 60], "title": "Elegant 1 verde"},
    10: {"boxes": [33, 34, 61], "title": "Elegant 1 crema"},
    11: {"boxes": [36, 37, 38], "title": "Elegant 2 verde"},
    12: {"boxes": [40, 41, 42], "title": "Elegant 2 crema"},
    13: {"boxes": [44, 45, 46], "title": "Elegant 3 verde"},
    14: {"boxes": [48, 49, 50], "title": "Elegant 3 crema"},
    15: {"boxes": [52, 62], "title": "Strelitzia"},
    16: {"boxes": [54, 64], "title": "Mango"},
    17: {"boxes": [55], "title": "Plumeria"},
    18: {"boxes": [56], "title": "Galleta Individual"},
}


def print_header(t="text/html"):
    print "Content-Type: " + t + ";charset=utf-8"
    print


def println(*lns):
    for ln in lns:
        print ln
    print "<br>"


def get_location():
    location = request.args.get('location', None)
    cookie_set = False
    if location is None:
        try:
            location = request.cookies['location']
            cookie_set = True
        except:
            location = 0
    return cookie_set, int(location)


def is_same_day(date1, date2):
    return datetime.strftime(date1, '%Y-%m-%d')\
           == datetime.strftime(date2, '%Y-%m-%d')


def earlier_than(hour, minute, dt):
    return dt < dt.replace(hour=hour, minute=minute)


def split_purchases(purchases):
    morning = {"ps": [], "total": {"cash": 0, "card": 0}}
    evening = {"ps": [], "total": {"cash": 0, "card": 0}}
    for p in purchases:
        if not earlier_than(17, 0, p['date']):
            morning['ps'].append(p)
        else:
            evening['ps'].append(p)
    return (morning, evening)


def calc_purchases_totals(ps):
    split_ps = split_purchases(ps)
    cash_total = 0
    card_total = 0
    for i, _ps in enumerate(split_ps):
        card_sum = 0
        cash_sum = 0
        ps = _ps['ps']
        for pk, p in enumerate(ps):
            ps[pk]['total'] = 0
            for ik, item in enumerate(p['cart']):
                ps[pk]['total'] += item['price'] * item['quantity']
                if p['card']:
                    card_sum += item['price'] * item['quantity']
                else:
                    cash_sum += item['price'] * item['quantity']
        split_ps[i]['total']['card'] = card_sum
        split_ps[i]['total']['cash'] = cash_sum
        cash_total += cash_sum
        card_total += card_sum
    return split_ps, (card_total, cash_total)


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
        elif str(e) == "'NoneType' object has no attribute 'strftime'":
            return None
        else:
            raise


def stringdate(string):
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')


def log(*lines):
    lines = [str(v) for v in lines]
    with open(os.path.join(app.root_path, 'log.txt'), 'a') as f:
        f.writelines('\n'.join(
            [jinja_filters.datetimeformat(datetime.now())]
            + lines
            + ["-----\n"]
        ))


def html_newlines(input_str):
    return input_str.replace("\n", br)


def only_admins(redirect_home=True):
    def decorator(func):
        from flask import flash, g, redirect, url_for, abort
        from flask_login import login_required

        @login_required
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not g.user.is_admin():
                if redirect_home:
                    flash("The requested page is only accessible by admins!",
                          "danger")
                    return redirect(url_for("home_page.home"))
                else:
                    abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 1ct = 100, 1€ = 100 00
def round_cent(x):
    return int(round(x / 100.0)) * 100
