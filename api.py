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
        else:
            date = convert_date(date_field + ":00")
            if date is None:
                return (False, "Not a valid datetime")
        discount_field = form.getfirst('discount')
        discount = 0 if discount_field is None else int(discount_field) 
        card = False if card is None else True
        insert_success = base.insert_purchase(country, card, date, discount, cookies)
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
    #sync_down()
    sync_up()
    # TODO combine return values
    return (False, "Not yet implemented")

def get_purchases():
    datestring = form.getfirst("last_update")
    if datestring is None:
        return (False, "You must give a date of the last update (last_update)")
    last_update = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
    purchases = base.get_purchases(prettydict=True, newerthan=last_update, datestring=True)
    return (True, json.dumps(purchases))

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
        (success, response) = save_purchase(base.get_boxes())
    elif action == "delete_purchase":
        success = delete_purchase()
    elif action == "get_purchases":
        (success, response) = get_purchases()
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
