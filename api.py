#!/usr/bin/python -u
# coding=utf-8
import cgitb
cgitb.enable()
import cgi
import json
from datetime import datetime
from dbconn import *
import requests
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import util
from dbdetails import dbdetails
form = cgi.FieldStorage()

def save_purchase(boxes):
    cookies = {} 
    for boxId, box in boxes.iteritems():
        boxId = str(boxId)
        count_field = form.getvalue('box_'+boxId) 
        count = 0 if count_field is None else int(count_field)
        if count > 0:
            cookies[boxId] = count
    if cookies:
        country  = form.getfirst('country')
        card     = form.getvalue('tarjeta')
        date_field = form.getfirst('datetime')
        if date_field is None:
            date = datetime.now() 
            edited = date
        else:
            date = convert_date(date_field + ":00")
            if date is None:
                return (False, "Not a valid datetime")
            edited = datetime.now()
        discount_field = form.getfirst('discount')
        discount = 0 if discount_field is None else int(discount_field) 
        card = False if card is None else True
        insert_success = base.insert_purchase(country, card, date, discount, cookies, edited)
        if insert_success:
            return (True, "Purchase saved")
    else:
        return (False, "No cookies")
    return (False, "Unknown save_purchase error")

def delete_purchase():
    syncId = form.getfirst('syncId')
    if syncId is not None:
        return base.mark_purchase_deleted(syncId)
    return False

def sync():
    downresult = sync_down()
    upresult = sync_up()
    generic_result = {"action": "sync"}
    generic_result.update(upresult)
    generic_result.update(downresult)
    return (True, generic_result)

def sync_down():
    edited = datetime.now()
    last_sync = base.get_last_sync()
    r = requests.get(dbdetails.serverroot+"/api.py", params={"action": "get_purchases", "last_update": last_sync})
    ps = r.json()
    result= {'synced_down': []}
    if "purchases" not in ps.keys():
        return result
    for p in ps['purchases']:
        purchase = p['purchase']
        cart = p['cart']
        syncId = purchase['syncId']
        existing = base.fetchone("purchases", ["status"], "WHERE syncId=" + str(syncId))
        if existing is None:
            if base.insert_purchase(purchase['country'], purchase['card'], purchase['date'], purchase['discount'], cart, edited, 3, syncId=syncId):
                result['synced_down'].append(syncId)
    base.update_last_sync(edited)
    return result

def sync_up():
    ps = base.get_purchases(getDeleted=True, datestring=True, prettydict=True, notsynced=True, simplecart=True)
    jsonstr = json.dumps(ps)
    r = requests.post(dbdetails.serverroot+"/api.py", params={"action": "syncUp"}, data={"data": jsonstr, "edited": util.datestring(datetime.now())})
    try:
        jresponse = r.json()
    except ValueError as e:
        print_text(r.text)
    for syncId in jresponse["deleted"]:
        base.delete_purchase(syncId)
    for syncId in jresponse["added"]:
        base.mark_synced(syncId)
    return {"deleted": jresponse['deleted'], "added": jresponse['added']}

def receive_sync_up():
    result = {"action": "syncUp", "deleted": [], "added": []}
    data = form.getfirst("data")
    edited = form.getfirst("edited")
    if edited is None:
        return (False, "You must have the edited thing set")
    ps = json.loads(data)
    for p in ps:
        purchase = p['purchase']
        cart = p['cart']
        status = purchase['status']
        syncId = purchase['syncId']
        existing = base.fetchone("purchases", ["status"], "WHERE syncId=" + str(syncId))
        if status == 0:
            if existing is None:
                if base.insert_purchase(purchase['country'], purchase['card'], purchase['date'], purchase['discount'], cart, edited, 3, syncId=syncId):
                    result['added'].append(syncId)
            elif existing == 2: # exists but was previously marked as deleted
                if base.change_status(syncId, 3):
                    result['added'].append(syncId)
        elif status == 2:
            if existing is None or base.delete_purchase(syncId):
                result['deleted'].append(syncId)
    return (True, json.dumps(result))

def get_purchases():
    datestring = form.getfirst("last_update")
    if datestring is None:
        return (False, "You must give a date of the last update (last_update)")
    last_update = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
    purchases = base.get_purchases(prettydict=True, newerthan=last_update, datestring=True, simplecart=True)
    return (True, json.dumps({"purchases": purchases}))

def convert_date(datestring):
    try:
        return datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
    except:
        try:
            datestring = datetime.now().strftime('%Y-%m-%d ') + datestring
            return datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
        except:
            pass
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
response = '{"result": "200 - OK"}'
if action is not None:
    if action == "save_purchase":
        (success, response) = save_purchase(base.get_boxes())
    elif action == "delete_purchase":
        success = delete_purchase()
    elif action == "get_purchases":
        (success, response) = get_purchases()
    elif action == "sync":
        (success, response) = sync()
    elif action == "syncUp":
        (success, response) = receive_sync_up() 
    else:
        print_text("No valid Action: " + str(action))
        action = None
else:
    print_text('{"result": "No Action"}')

if success:
    redirect = form.getfirst('redirect')
    if redirect is None:
        print_text(response)
    else:
        print "Location: " + redirect
        print 
elif action is not None:
    print_text('{"result": "No success - ' + response + '", "action": "' + action + '"}')
