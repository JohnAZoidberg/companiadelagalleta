#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

import json
from datetime import datetime
import requests

from dbconn import CgBase
import util
from dbdetails import dbdetails

from flask import Blueprint, request, redirect, url_for, jsonify, abort


api_page = Blueprint('api_page', __name__, template_folder='templates')


@api_page.route('/api/v1.0/purchases', methods=['POST'])
def save_purchase(boxes):
    base = CgBase(util.get_location()[1])
    cookies = {}
    for boxId, box in boxes.iteritems():
        boxId = str(boxId)
        count_field = form.getvalue('box_'+boxId)
        count = 0 if count_field is None else int(count_field)
        if count > 0:
            cookies[boxId] = count
    if cookies:
        country = form.getfirst('country')
        card = form.getvalue('payment')
        note = form.getvalue('note')
        note = "" if note is None else note
        date_field = form.getfirst('date') + " " + form.getfirst('time')
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
        insert_success = base.insert_purchase(country, card, date, discount,
                                              cookies, edited, note=note,
                                              updateStock=True)
        if insert_success:
            resp = jsonify(data)
            resp.status_code = 201
            return resp
    else:
        return (False, "No cookies")
    return (False, "Unknown save_purchase error")


@api_page.route('/api/v1.0/purchases/<int:sync_id>', methods=['DELETE'])
def delete_purchase():
    base = CgBase(util.get_location()[1])
    success = base.mark_purchase_deleted(sync_id, updateStock=True)
    if success:
        return jsonify({"purchase_deleted": sync_id})
    else:
        return abort_msg(404, "Not purchase with syncId: " + str(sync_id))



def sync():
    downresult = sync_down()
    upresult = sync_up()
    generic_result = {"action": "sync"}
    generic_result.update(upresult)
    generic_result.update(downresult)
    return (True, generic_result)


def sync_down():
    base = CgBase(util.get_location()[1])
    edited = datetime.now()
    last_sync = base.get_last_sync()
    r = requests.get(dbdetails.serverroot+"/api.py",
                     params={"action": "sync_down", "last_update": last_sync})
    try:
        jres = r.json()
        ps = jres["purchases"]
    except TypeError:
        jres = json.loads(jres)
    except:
        print_text("ERROR ON SERVERSIDE!<br>"+r.text)
        exit()
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
        existing = base.fetchone("purchases", ["status"],
                                 ("WHERE syncId = %s", syncId))
        if status == 2:
            if base.delete_purchase(syncId):
                result['synced_down']['purchases']['deleted'].append(syncId)
        else:
            if existing is None:
                if base.insert_purchase(purchase['country'], purchase['card'],
                                        purchase['date'], purchase['discount'],
                                        cart, edited,
                                        location=purchase['location'],
                                        status=3, syncId=syncId,
                                        note=purchase['note']):
                    result['synced_down']['purchases']['added'].append(syncId)
            else:
                result['synced_down']['purchases']['deleted'].append(syncId)

    # shifts
    shifts = jres["shifts"]
    for shift in shifts:
        syncId = shift['syncId']
        status = shift['status']
        existing = base.fetchone("shifts", ["status"],
                                 ("WHERE syncId = %s", syncId))
        if status == 2:
            if base.delete_shift(syncId):
                result['synced_down']['shifts']['deleted'].append(syncId)
        else:
            if existing is None:
                if base.insert_shift(shift["workerId"], shift["start"],
                                    shift["end"], edited,
                                    location=shift["location"],
                                    status=3, syncId=syncId):
                    result['synced_down']['shifts']['added'].append(syncId)
            else:
                result['synced_down']['shifts']['deleted'].append(syncId)
    # stock
    stock = jres["stock"]
    for container in stock:
        syncId = container['syncId']
        status = container['status']
        if status == 1:
            if base.update_container(
                    syncId, container['containerId'],
                    container['quantity'], container['location'],
                    edited, util.stringdate(container['recounted'])):
                result['synced_down']['stock']['edited'].append(syncId)
    base.update_last_sync(edited)
    return result


def receive_sync_down():
    base = CgBase(util.get_location()[1])
    datestring = form.getfirst("last_update")
    if datestring is None:
        return (False, "You must give a date of the last update (last_update)")
    last_update = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
    result = {}
    result['purchases'] = base.get_purchases(
        prettydict=True, newerthan=last_update, datestring=True,
        simplecart=True, getDeleted=True, allLocations=True)
    result['shifts'] = base.get_shifts(
        getDeleted=True, datestring=True,
        newerthan=last_update, allLocations=True)
    result['stock'] = base.get_stock(datestring=True, newerthan=last_update,
                                     allLocations=True)
    return (True, json.dumps(result))


def sync_up():
    base = CgBase(util.get_location()[1])
    ps = base.get_purchases(getDeleted=True, datestring=True, prettydict=True,
                            notsynced=True, simplecart=True, allLocations=True)
    shifts = base.get_shifts(getDeleted=True, datestring=True, notsynced=True,
                             allLocations=True)
    stock = base.get_stock(datestring=True, notsynced=True, allLocations=True)
    syncdata = {"purchases": ps, "shifts": shifts, "stock": stock}
    jsonstr = json.dumps(syncdata)
    r = requests.post(dbdetails.serverroot+"/api.py",
                      params={"action": "syncUp"}, data={
                          "data": jsonstr,
                          "edited": util.datestring(datetime.now())
                      }
    )
    try:
        jres = r.json()
        foo = jres['purchases']
    except TypeError:
        jres = json.loads(jres)
    except:
        print_text("ERROR ON SERVERSIDE!<br>\n" + r.text)
        exit()
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
        "purchases": {"deleted": jres["purchases"]['deleted'],
                      "added": jres["purchases"]['added']},
        "shifts": {"deleted": jres["shifts"]['deleted'],
                   "added": jres["shifts"]['added']},
        "stock": {"edited": jres["stock"]['edited']}
    }}


def receive_sync_up():
    base = CgBase(util.get_location()[1])
    result = {
        "action": "syncUp",
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
        existing = base.fetchone("purchases", ["status"],
                                 ("WHERE syncId = %s", syncId))
        if status == 0:
            if existing is None:
                if base.insert_purchase(
                        purchase['country'], purchase['card'], purchase['date'],
                        purchase['discount'], cart, edited,
                        location=purchase['location'], status=3, syncId=syncId,
                        note=purchase['note']):
                    result["purchases"]['added'].append(syncId)
            else:
                if existing == 2:  # exists but was previously marked as deleted
                    if base.change_purchase_status(syncId, 3):
                        result["purchases"]['added'].append(syncId)
                else:
                    result["purchases"]['added'].append(syncId)
        elif status == 2:
            base.mark_purchase_deleted(syncId)
            result["purchases"]['deleted'].append(syncId)
    # shifts
    shifts = res["shifts"]
    for shift in shifts:
        syncId = shift['syncId']
        status = shift['status']
        existing = base.fetchone("shifts", ["status"],
                                 ("WHERE syncId = %s", syncId))
        if status == 0:
            if existing is None:
                if base.insert_shift(
                        shift["workerId"], shift["start"], shift["end"], edited,
                        location=shift["location"], status=3, syncId=syncId):
                    result["shifts"]['added'].append(syncId)
            else:
                if existing == 2:  # exists but was previously marked as deleted
                    if base.change_shift_status(syncId, 3):
                        result["shifts"]['added'].append(syncId)
                else:
                    result["shifts"]['added'].append(syncId)
        elif status == 2:
            base.mark_shift_deleted(syncId)
            result["shifts"]['deleted'].append(syncId)
    # stock
    stock = res["stock"]
    for container in stock:
        syncId = container['syncId']
        status = container['status']
        if status == 1:
            if base.update_container(
                    syncId, container['containerId'], container['quantity'],
                    container['location'], util.stringdate(container['edited']),
                    util.stringdate(container['recounted'])):
                result["stock"]['edited'].append(syncId)

    return (True, json.dumps(result))


@api_page.route('/api/v1.0/shifts/<int:worker_id>/begin',
                methods=['PUT'])
def begin_work(worker_id):
    base = CgBase(util.get_location()[1])
    workres = base.begin_work(worker_id)
    if workres:
        return jsonify({"work_started": worker_id})
    else:
        message = {
                'status': 500,
                'message': "Unknown start work error",
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp


@api_page.route('/api/v1.0/shifts/<int:worker_id>/end',
                methods=['PUT'])
def end_work(worker_id):
    base = CgBase(util.get_location()[1])
    workres = base.end_work(worker_id)
    if workres:
        return jsonify({"work_ended": worker_id})
    else:
        message = {
                'status': 404,
                'message': "Worker hasn't started: " + str(worker_id),
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp


@api_page.route('/api/v1.0/stock', methods=['POST'])
def update_stock():
    base = CgBase(util.get_location()[1])
    method = request.form.get('count-method', None)
    if method == "relative":
        absolute = False
    elif method == "absolute":
        absolute = True
    else:
        return abort_msg(400, "Wrong method for stock update")
    containers = {}
    for containerId in util.containers.keys():
        containerId = str(containerId)
        count_field = request.form.get('container_' + containerId, 0)
        count = int(count_field)
        if absolute or not count == 0:
            containers[containerId] = count
    success = base.update_stock(containers, absolute)
    if success:
        redirect_target = request.form.get('redirect', None)
        if redirect_target is not None:
            return redirect(url_for('stock_page.stock'))
        else:
            return jsonify({"updated_stock": containers})
    else:
        return abort_msg(500, "Some stock update error")


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

def abort_msg(status, msg):
        message = {
                'status': status,
                'message': msg,
        }
        resp = jsonify(message)
        resp.status_code = status
        return resp
