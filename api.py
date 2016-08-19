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
import jinja_filters

from flask import Blueprint, request, redirect, url_for, jsonify


api_page = Blueprint('api_page', __name__, template_folder='templates')


@api_page.route('/api/v1.0/purchase', methods=['POST'])
def save_purchase():
    purchase = request.get_json()
    base = CgBase(util.get_location()[1])
    if purchase['boxes']:
        date = convert_date(purchase['datetime'] + ":00")
        if date is None:
            return abort_msg(400, "Not a valid datetime")
        edited = datetime.now()
        insert_success = base.insert_purchase(
            purchase['country'], purchase['card'], purchase['datetime'],
            purchase['discount'], purchase['boxes'], edited,
            note=purchase['note'])
        if insert_success:
            resp = jsonify({"save_purchase": "Successful"})
            resp.status_code = 201
            return resp
    else:
        return abort_msg(400, "No cookies")
    return abort_msg(400, "Unknown save_purchase error")


@api_page.route('/api/v1.0/purchase/<int:sync_id>', methods=['DELETE'])
def delete_purchase(sync_id):
    base = CgBase(util.get_location()[1])
    success = base.mark_purchase_deleted(sync_id)
    if success:
        return jsonify({"purchase_deleted": sync_id})
    else:
        return abort_msg(404, "Not purchase with syncId: " + str(sync_id))

@api_page.route('/api/v1.0/sync', methods=['GET', 'PUT'])
def sync():
    base = CgBase(util.get_location()[1])
    if not dbdetails.server:  # Clientside
        # get data to return
        up_data = {
            "data": {},
            "sync_time": util.datestring(datetime.now()),
            "last_sync": util.datestring(base.get_last_sync())
        }
        up_data['data']['purchase'] = base.get_purchases(
                getDeleted=True, datestring=True, prettydict=True,
                notsynced=True, simplecart=True, allLocations=True)
        up_data['data']['shift'] = base.get_shifts(
                getDeleted=True, datestring=True, notsynced=True,
                allLocations=True)
        up_data['data']['stock'] = base.get_stock(
                datestring=True, notsynced=True, allLocations=True)
        r = requests.put(dbdetails.serverroot + "/api/v1.0/sync",
                        data=json.dumps(up_data),
                        headers={"Content-Type": "application/json"}
        )
        # TODO mark everything as synced (status = 3)
        # TODO write synced items to log file
        try:
            input = r.json()
            synced_up = input['synced']
            down_data = input['data']
        except ValueError:
            try:
                input = json.loads(r.text)
            except ValueError:
                return ("ERROR ON SERVERSIDE!<br>\n" + r.text)
            except:
                raise
        except:
            raise
        sync_time = datetime.now()
    else: # Serverside
        input = request.get_json()
        try:
            sync_time = util.stringdate(input['sync_time'])
        except:
            return "JSON ERROR: " + str(input)

    # update based on submitted data
    existing = []
    purchase_items = input['data']['purchase']
    if purchase_items:
        extra = ("WHERE syncId IN (%s" + (",%s"*(len(purchase_items)-1)) + ")",
                tuple(item['syncId'] for item in purchase_items))
        existing += base.fetchall("purchases", ["syncId", "status", "edited"],
                                 extra)
    shift_items = input['data']['shift']
    if shift_items:
        extra = ("WHERE syncId IN (%s" + (",%s"*(len(shift_items)-1)) + ")",
                tuple(item['syncId'] for item in shift_items))
        existing += base.fetchall("shifts", ["syncId", "status", "edited"],
                                 extra)
    stock_items = input['data']['stock']
    if stock_items:
        extra = ("WHERE syncId IN (%s" + (",%s"*(len(stock_items)-1)) + ")",
                tuple(item['syncId'] for item in stock_items))
        existing += base.fetchall("stock", ["syncId", "status", "edited"],
                                 extra)
    existing = {x[0]: x for x in existing}
    synced = {
            "added": {"purchase": [], "shift": [], "stock": []},
            "edited": {"purchase": [], "shift": [], "stock": []},
            "deleted": {"purchase": [], "shift": [], "stock": []}
    }
    for _type, item_list in input['data'].iteritems():
        for item in item_list:
            status = item['status']
            sync_id = item['syncId']
            edited = util.stringdate(item['edited'])
            existing_status = None
            try:
                existing_status = existing[sync_id][1]  # ['status']
                existing_edited = existing[sync_id][2]  # ['edited']
            except KeyError:
                existing_status = None
            if status == 0:
                insert_item(base, _type, item, sync_time)
                synced['added'][_type].append(sync_id)
            elif status == 1:
                if existing_status == 0:
                    edit_item(base, _type, item, sync_time)
                elif (existing_status == 1
                     or existing_status == 2
                     or existing_status == 3):
                    if edited > existing_edited:
                        edit_item(base, _type, item, sync_time)
                elif existing_status is None:
                    insert_item(base, _type, item, sync_time)
                synced['edited'][_type].append(sync_id)
            elif status == 2:
                if existing_status == 0:
                    delete_item(base, _type, item, sync_time)
                elif existing_status == 1 or existing_status == 3:
                    if edited > existing_edited:
                        delete_item(base, _type, item, sync_time)
                elif existing_status == 2:
                    if edited > existing_edited:
                        edit_item(base, _type, item, sync_time)
                elif existing_status is None:
                    insert_item(base, _type, item, sync_time)
                synced['deleted'][_type].append(sync_id)

    if dbdetails.server:
        # get data to return
        last_sync = util.stringdate(input['last_sync'])
        result = {"data": {}, "synced": synced}
        result['data']['purchase'] = base.get_purchases(
            prettydict=True, newerthan=last_sync, datestring=True,
            simplecart=True, getDeleted=True, allLocations=True,
            notnow=sync_time)
        result['data']['shift'] = base.get_shifts(
            getDeleted=True, datestring=True,
            newerthan=last_sync, allLocations=True, notnow=sync_time)
        result['data']['stock'] = base.get_stock(
                datestring=True, newerthan=last_sync,
                allLocations=True, notnow=sync_time)
        return jsonify(result)
    else:
        for action, types in synced_up.iteritems():
            for _type, items in types.iteritems():
                for sync_id in items:
                    if _type == "purchase":
                        if action == "deleted":
                            base.delete_purchase(sync_id)
                        else:
                            base.mark_purchase_synced(sync_id)
                    elif _type == "shift":
                        if action == "deleted":
                            base.delete_shift(sync_id)
                        else:
                            base.mark_shift_synced(sync_id)
                    elif _type == "stock":
                        if action == "deleted":
                            pass # not possible to delete stock
                        else:
                            base.mark_container_synced(sync_id)
        base.update_last_sync(sync_time)
        sync_summary = {"synced_up": synced_up, "synced_down": synced}
        sync_msg = handle_sync_result(sync_summary)
        with open('log.txt', 'a') as f:
            f.writelines('\n'.join([
                jinja_filters.datetimeformat(datetime.now()),
                #"shellupdate:",
                #str(shell_updatestr),
                "updatemsg:",
                str(sync_msg),
                "sync",
                json.dumps(sync_summary),
                "-----\n"
            ]))
        return redirect("/home?msg=" + sync_msg)

def handle_sync_result(sync_summary):
    if (not sync_summary['synced_down']['deleted']['purchase']
            and not sync_summary['synced_down']['added']['purchase']
            and not sync_summary['synced_down']['edited']['purchase']
            and not sync_summary['synced_up']['deleted']['purchase']
            and not sync_summary['synced_up']['added']['purchase']
            and not sync_summary['synced_up']['edited']['purchase']
            and not sync_summary['synced_down']['deleted']['shift']
            and not sync_summary['synced_down']['added']['shift']
            and not sync_summary['synced_down']['edited']['shift']
            and not sync_summary['synced_up']['deleted']['shift']
            and not sync_summary['synced_up']['added']['shift']
            and not sync_summary['synced_up']['edited']['stock']
            and not sync_summary['synced_down']['deleted']['shift']
            and not sync_summary['synced_down']['added']['shift']
            and not sync_summary['synced_down']['edited']['stock']):
        return "Nothing to sync"
    else:
        return "Sync done"

def insert_item(base, _type, item, sync_time):
    status = 0 if dbdetails.server else 3
    if _type == "purchase":
        base.insert_purchase(item['country'], item['card'], item['date'],
                item['discount'], item['cart'], sync_time,
                location=item['location'], status=status,
                syncId=item['syncId'], note=item['note'])
        pass
    elif _type == "shift":
        base.insert_shift(item['workerId'], item['start'], item['end'],
                sync_time, location=item['location'], status=status,
                syncId=item['syncId'])
        pass
    elif _type == "stock":
        pass  # it is not possible to insert stock


def edit_item(base, _type, item, sync_time):
    if item['status'] == 2:
        status = 2
    elif dbdetails.server:
        status = 1
    else:
        status = 3
    if _type == "purchase":
        base.update_purchase(item['country'], item['card'], item['date'],
                item['discount'], item['cart'], sync_time,
                location=item['location'], status=status,
                syncId=item['syncId'], note=item['note'])
    elif _type == "shift":
        pass  # it is not possible to edit a shift
    elif _type == "stock":
        base.update_container(item['syncId'], item['containerId'],
                item['quantity'], item['location'], sync_time,
                item['recounted'], status=status)


def delete_item(base, _type, item, sync_time):
    sync_id = item['syncId']
    if _type == "purchase":
        if dbdetails.server:
            base.mark_purchase_deleted(sync_id)
        else:
            base.delete_purchase(sync_id)
    elif _type == "shift":
        if dbdetails.server:
            base.mark_shift_deleted(sync_id)
        else:
            base.delete_shift(sync_id)
    elif _type == "stock":
        pass  # it is not possible to delete stock


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
def begin_(worker_id):
    base = CgBase(util.get_location()[1])
    workres = base.begin_work(worker_id)
    if workres:
        return jsonify({
            "worker_id": worker_id,
            "end": None
        })
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
    if not workres:
        message = {
                'status': 404,
                'message': "Worker hasn't started: " + str(worker_id),
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    else:
        return jsonify({
            "worker_id": worker_id
        })


@api_page.route('/api/v1.0/stock/form', methods=['POST'])
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
        count = int(request.form.get('container_' + containerId, 0))
        old_count = int(request.form.get('old_' + containerId, 0))
        if (absolute and count != old_count) or not count == 0:
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
