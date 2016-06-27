#!/usr/bin/python -u
# coding=utf-8
import cgitb
cgitb.enable()
import cgi
import json
from datetime import datetime
from dbconn import *
import urllib2
import urllib
from asyncRequests import AsyncRequests
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import util
form = cgi.FieldStorage()

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
        return base.mark_purchase_deleted(syncId)
    return False

def sync():
    ps = base.get_purchases(True) 
    urls = []
    for p in ps:
        (syncId, status, country, card, discount, date) = p['purchase']
        datestring = date.strftime('%Y-%m-%d %H:%M:%S') 
        if status == 0: # new entry
            params = {"action": "syncPurchase", "syncId": str(syncId), "country": country, "card": str(card), "discount": str(discount), "date": datestring, "status": str(status)}
            url = "http://46.101.112.121/api.py?" + urllib.urlencode(params)
            urls.append(url)
            for item in p['cart']:
                (title, status, boxId, quantity, price) = item
                cparams = {"action": "syncCart", "syncId": str(syncId), "status": str(status), "boxId": str(boxId), "quantity": str(quantity), "price": str(price)}
                url =  "http://46.101.112.121/api.py?" + urllib.urlencode(cparams)
                urls.append(url)
    if not urls:
        return (True, '{"result": "Nothing to sync"}')
    results = []
    for url in urls:
        results.append(urllib2.urlopen(url))
    synced = {}
    synced['purchase'] = 0
    synced['cart'] = 0
    for result in results:
        resultstr = result.read()
        jresult = json.loads(resultstr)
        result_type = jresult['result']
        if result_type == "200 - SYNCED PURCHASE":
            base.mark_synced(jresult['syncId'])
            synced['purchase'] += 1
        if result_type == "200 - SYNCED CART":
            base.mark_synced(jresult['syncId'], jresult['boxId'])
            synced['cart'] += 1
    if synced['cart'] + synced['purchase'] > 0:
        return (True, '{"result": "SYNC completed (' + str(synced['purchase']) + ', ' + str(synced['cart']) + ')"}') 
    return (False, None)

def sync_cart():
    syncId = int(form.getfirst("syncId"))
    status = int(form.getfirst("status"))
    boxId  = int(form.getfirst("boxId"))
    quantity = int(form.getfirst("quantity"))
    price = int(form.getfirst("price"))
    success = base.sync_cart(syncId, status, boxId, quantity, price)
    return (success, '{"result": "200 - SYNCED CART", "syncId": ' + str(syncId) + ', "boxId": ' + str(boxId) + '}')

def sync_purchase():
    syncId = int(form.getfirst("syncId"))
    country = form.getfirst("country")
    card = bool(int(form.getfirst("card")))
    discount = int(form.getfirst("discount"))
    datestring = form.getfirst("date")
    date = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
    status = int(form.getfirst("status"))
    success = base.sync_purchase(syncId, status, country, card, discount, date)
    return (success, '{"result": "200 - SYNCED PURCHASE", "syncId": ' + str(syncId) + '}')

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

def chunk(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

base = CgBase()
action = form.getfirst("action")
success = False
response = '{"result": "200 - OK"}'
if action is not None:
    if action == "save_purchase":
        success = save_purchase()
    elif action == "delete_purchase":
        success = delete_purchase()
    elif action == "sync":
        (success, response) = sync()
    elif action == "syncCart":
        (success, response) = sync_cart() 
    elif action == "syncPurchase":
        (success, response) = sync_purchase() 
    else:
        print_text("No valid Action: " + str(action))
        action = None
else:
    print_text("No Action")

if success:
    redirect = form.getfirst('redirect')
    if redirect is None:
        print_text(response)
    else:
        print "Location: " + redirect
        print 
elif action is not None:
    print_text('{"result": "No success - ' + action + '"}')
