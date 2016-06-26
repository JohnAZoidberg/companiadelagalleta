#!/usr/bin/python -u
# coding=utf-8
import cgitb
cgitb.enable()
import cgi
import json
from datetime import datetime
from dbconn import *
import urllib
from asyncRequests import AsyncRequests
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import util
form = cgi.FieldStorage()
action_result = '{"result": "200 - OK"}' 

def save_purchase():
    cookies = {} 
    for box in xrange(1, 1+len(util.cookie_list)):
        box = str(box)
        count_field = form.getvalue('box_'+box) 
        count = 0 if count_field is None else int(count_field)
        if count > 0:
            cookies[box] = count
    if cookies:
        country  = form.getfirst('country')
        card     = form.getvalue('tarjeta')
        date_field = form.getfirst('datetime')
        if date_field is None:
            date = datetime.now() 
        else:
            date = convert_date(date_field + ":00")
        discount = int(form.getfirst('discount')) 
        card = False if card is None else True
        base.insert_purchase(country, card, date, discount, cookies)
        return True
    else:
        print_text("No cookies")
    return False

def delete_purchase():
    syncId = form.getfirst('syncId')
    if syncId is not None:
        return base.delete_purchase(syncId)
    return False

def sync():
    print_text("")
    br = "<br>"
    ps = base.get_purchases() 
    urls = []
    for p in ps:
        (syncId, status, country, card, discount, date) = p['purchase']
        datestring = date.strftime('%Y-%m-%d %H:%M:%S') 
        if status == 3:
            continue
        params = {"action": "syncPurchase", "syncId": str(syncId), "country": country, "card": str(card), "discount": str(discount), "date": datestring, "status": str(status)
        urls.append("http://46.101.112.121/api.py?" + urllib.urlencode(params))
        for item in p['cart']:
            (title, status, boxId, quantity, price) = item
            cparams = {"action": "syncCart", "syncId": str(syncId), "status": str(status), "boxId": str(boxId), "quantity": str(quantity), "price": str(price)}
            urls.append("http://46.101.112.121/api.py?" + urllib.urlencode(cparams))
    with AsyncRequests() as request:
        request.run(urls)
        for result in request.results:
            try:
                print result.read(), br
            except:
                print result, br
    return False

def sync_purchase():
    syncId = int(form.getfirst("syncId"))
    country = form.getfirst("country")
    card = bool(form.getfirst("card"))
    discount = int(form.getfirst("discount"))
    datestring = form.getfirst("date")
    date = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
    status = int(form.getfirst("status"))
    return base.sync_purchase(syncId, status, country, card, discount, date)

def convert_date(datestring):
    try:
        return datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
    except:
        try:
            datestring = datetime.now().strftime('%Y-%m-%d ') + datestring
            return datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
        except:
            print_text("Not a valid datetime! (" + datestring + ")")
    return None

def print_json(text):
    util.print_header("text/json")
    print text

def print_text(text):
    util.print_header()
    print text

base = CgBase()
action = form.getfirst("action")
success = False
if action is not None:
    if action == "save_purchase":
        success = save_purchase()
    elif action == "delete_purchase":
        success = delete_purchase()
    elif action == "sync":
        success = sync()
    elif action == "syncPurchase":
        success = sync_purchase() 
        if success:
            action_result = '{"result": "200 - SYNCED"}'
    else:
        print_text("No valid Action: " + str(action))
        action = None
else:
    print_text("No Action")

if success:
    redirect = form.getfirst('redirect')
    if redirect is None:
        print_text(action_result)
    else:
        print "Location: " + redirect
        print 
elif action is not None:
    print_text("No success - " + action)
