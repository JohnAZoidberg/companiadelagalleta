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
    else:
        print_text("No valid Action")
else:
    print_text("No Action")

if success:
    redirect = form.getfirst('redirect')
    if redirect is None:
        cg.print_header()
        print_text('{"result": "200 - OK"}')
    else:
        print "Location: " + redirect
        print 
