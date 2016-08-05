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
base = CgBase(util.get_location())

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
        card     = form.getvalue('payment')
        date_field = form.getfirst('date')  + " " + form.getfirst('time')
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
        card = True if card == "card" else False
        insert_success = base.insert_purchase(country, card, date, discount, cookies, edited, updateStock=True)
        if insert_success:
            return (True, "Purchase saved")
    else:
        return (False, "No cookies")
    return (False, "Unknown save_purchase error")

def delete_purchase():
    syncId = form.getfirst('syncId')
    if syncId is not None:
        return base.mark_purchase_deleted(syncId, updateStock=True)
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
    r = requests.get(dbdetails.serverroot+"/api.py", params={"action": "sync_down", "last_update": last_sync})
    try:
        jres = r.json()
        foo = jres["purchases"]
    except ValueError as e:
        print_text("ERROR ON SERVERSIDE!<br>"+r.text)
        exit()
    except TypeError:
        jres = json.loads(jres)
    result = {'synced_down': {
        "purchases": {"added": [], "deleted": []},
        "shifts":    {"added": [], "deleted": []},
        "stock":     {"edited": []},
    }}
    # purchases
    ps = jres["purchases"]
    for p in ps:
        purchase = p['purchase']
        cart = p['cart']
        syncId = purchase['syncId']
        status = purchase['status']
        existing = base.fetchone("purchases", ["status"], "WHERE syncId=" + str(syncId))
        if status == 2:
            if base.delete_purchase(syncId):
                result['synced_down']['purchases']['deleted'].append(syncId)
        elif existing is None:
            if base.insert_purchase(purchase['country'], purchase['card'], purchase['date'], purchase['discount'], cart, edited, location=purchase['location'], status=3, syncId=syncId):
                result['synced_down']['purchases']['added'].append(syncId)
    # shifts
    shifts = jres["shifts"]
    for shift in shifts:
        syncId = shift['syncId']
        status = shift['status']
        existing = base.fetchone("shifts", ["status"], "WHERE syncId=" + str(syncId))
        if status == 2:
            if base.delete_shift(syncId):
                result['synced_down']['shifts']['deleted'].append(syncId)
        elif existing is None:
            if base.insert_shift(shift["workerId"], shift["start"], shift["end"], edited, location=shift["location"], status=3, syncId=syncId):
                result['synced_down']['shifts']['added'].append(syncId)
    # stock
    stock = jres["stock"]
    for container in stock:
        syncId = container['syncId']
        status = container['status']
        if status == 1:
            if base.update_container(syncId, container['containerId'], container['quantity'], container['location'], edited, util.stringdate(container['recounted'])):
                result['synced_down']['stock']['edited'].append(syncId)
    base.update_last_sync(edited)
    return result

def receive_sync_down():
    datestring = form.getfirst("last_update")
    if datestring is None:
        return (False, "You must give a date of the last update (last_update)")
    last_update = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
    result = {}
    result['purchases'] = base.get_purchases(prettydict=True, newerthan=last_update, datestring=True, simplecart=True, getDeleted=True, allLocations=True)
    result['shifts'] = base.get_shifts(getDeleted=True, datestring=True, newerthan=last_update, allLocations=True)
    result['stock'] = base.get_stock(datestring=True, newerthan=last_update, allLocations=True)
    return (True, json.dumps(result))

def sync_up():
    ps = base.get_purchases(getDeleted=True, datestring=True, prettydict=True, notsynced=True, simplecart=True, allLocations=True)
    shifts = base.get_shifts(getDeleted=True, datestring=True, notsynced=True, allLocations=True)
    stock = base.get_stock(datestring=True, notsynced=True, allLocations=True)
    syncdata = {"purchases": ps, "shifts": shifts, "stock": stock}
    jsonstr = json.dumps(syncdata)
    r = requests.post(dbdetails.serverroot+"/api.py", params={"action": "syncUp"}, data={"data": jsonstr, "edited": util.datestring(datetime.now())})
    try:
        jres = r.json()
        foo = jres["purchases"]
    except ValueError as e:
        print_text("ERROR ON SERVERSIDE!<br>\n" + r.text)
        exit()
    except TypeError:
        jres = json.loads(jres)
    # handle result - mark deleted or as synced
    # purchases
    for syncId in jres["purchases"]["deleted"]:
        base.delete_purchase(syncId)
    for syncId in jres["purchases"]["added"]:
        base.mark_purchase_synced(syncId)
    # shifts
    for syncId in jres["shifts"]["deleted"]:
        base.delete_shift(syncId)
    for syncId in jres["shifts"]["added"]:
        base.mark_shift_synced(syncId)
    # stock
    for syncId in jres["stock"]["edited"]:
        base.mark_container_synced(syncId)
    return {"synced_up": {
        "purchases": {"deleted": jres["purchases"]['deleted'], "added": jres["purchases"]['added']},
        "shifts": {"deleted": jres["shifts"]['deleted'], "added": jres["shifts"]['added']},
        "stock": {"edited": jres["stock"]['edited']}
    }}

def receive_sync_up():
    result = {"action": "syncUp",
        "purchases": {"deleted": [], "added": []},
        "shifts":    {"deleted": [], "added": []},
        "stock":    {"edited": []}
    }
    data = form.getfirst("data")
    edited = form.getfirst("edited")
    if edited is None:
        return (False, "You must have the edited thing set")

    res = json.loads(data)
    # purchases
    ps = res["purchases"]
    for p in ps:
        purchase = p['purchase']
        cart = p['cart']
        status = purchase['status']
        syncId = purchase['syncId']
        existing = base.fetchone("purchases", ["status"], "WHERE syncId=" + str(syncId))
        if status == 0:
            if existing is None:
                if base.insert_purchase(purchase['country'], purchase['card'], purchase['date'], purchase['discount'], cart, edited, location=purchase['location'], status=3, syncId=syncId):
                    result["purchases"]['added'].append(syncId)
            elif existing == 2: # exists but was previously marked as deleted
                if base.change_purchase_status(syncId, 3):
                    result["purchases"]['added'].append(syncId)
        elif status == 2:
            if existing is None or base.mark_purchase_deleted(syncId):
                result["purchases"]['deleted'].append(syncId)
    # shifts
    shifts = res["shifts"]
    for shift in shifts:
        syncId = shift['syncId']
        status = shift['status']
        existing = base.fetchone("shifts", ["status"], "WHERE syncId=" + str(syncId))
        if status == 0:
            if existing is None:
                if base.insert_shift(shift["workerId"], shift["start"], shift["end"], edited, location=shift["location"], status=3, syncId=syncId):
                    result["shifts"]['added'].append(syncId)
            elif existing == 2: # exists but was previously marked as deleted
                if base.change_shift_status(syncId, 3):
                    result["shifts"]['added'].append(syncId)
        elif status == 2:
            if existing is None or base.mark_shift_deleted(syncId):
                result["shifts"]['deleted'].append(syncId)
    # stock
    stock = res["stock"]
    for container in stock:
        syncId = container['syncId']
        status = container['status']
        if status == 1:
            if base.update_container(syncId, container['containerId'], container['quantity'], container['location'], util.stringdate(container['edited']), util.stringdate(container['recounted'])):
                result["stock"]['edited'].append(syncId)

    return (True, json.dumps(result))

def begin_work():
    workerId = form.getfirst("workerId")
    workres = base.begin_work(workerId)
    return (workres, {"work_started": workerId})

def end_work():
    workerId = form.getfirst("workerId")
    workres = base.end_work(workerId)
    return (workres, {"work_ended": workerId})

def update_stock():
    method = form.getfirst("count-method")
    if method is None:
        return (False, "Wrong method for stock update")
    elif method == "relative":
        absolute = False
    elif method == "absolute":
        absolute = True
    else:
        return (False, "Wrong method for stock update")
    containers = {}
    for containerId in util.containers.keys():
        containerId = str(containerId)
        count_field = form.getvalue('container_' + containerId)
        count = int(count_field)
        if absolute or not count == 0:
            containers[containerId] = count
    success = base.update_stock(containers, absolute)
    if success:
        return (True, "Stock updated")
    else:
        return (False, "Some stock update error")

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

if __name__ == "__main__":
    action = form.getfirst("action")
    success = False
    response = '{"result": "200 - OK"}'
    if action is not None:
        if action == "save_purchase":
            (success, response) = save_purchase(base.get_boxes())
        elif action == "delete_purchase":
            success = delete_purchase()
        elif action == "sync_down":
            (success, response) = receive_sync_down()
        elif action == "sync":
            (success, response) = sync()
        elif action == "syncUp":
            (success, response) = receive_sync_up()
        elif action == "begin_work":
            (success, response) = begin_work()
        elif action == "end_work":
            (success, response) = end_work()
        elif action == "update_stock":
            (success, response) = update_stock()
        else:
            print_text("No valid Action: " + str(action))
            action = None
    else:
        print_text('{"result": "No Action"}')

    if success:
        redirect = form.getfirst('redirect')
        if redirect is None:
            print_text(json.dumps(response))
        else:
            print "Location: " + redirect
            print
    elif action is not None:
        print_text('{"result": "No success - ' + str(response) + '", "action": "' + action + '"}')
