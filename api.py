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
                getDeleted=True, datestring=True, notsynced=True,
                simplecart=True, allLocations=True)
        up_data['data']['shift'] = base.get_shifts(
                getDeleted=True, datestring=True, notsynced=True,
                allLocations=True)
        up_data['data']['stock'] = base.get_stock_items(
                datestring=True, notsynced=True, allLocations=True)
        r = requests.put(dbdetails.serverroot + "/api/v1.0/sync",
                        data=json.dumps(up_data),
                        headers={"Content-Type": "application/json"}
        )
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
                if existing_status is None:
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
    base.db.commit()

    if dbdetails.server:
        # get data to return
        last_sync = util.stringdate(input['last_sync'])
        result = {"data": {}, "synced": synced}
        result['data']['purchase'] = base.get_purchases(
            newerthan=last_sync, datestring=True,
            simplecart=True, getDeleted=True, allLocations=True,
            notnow=sync_time)
        result['data']['shift'] = base.get_shifts(
            getDeleted=True, datestring=True,
            newerthan=last_sync, allLocations=True, notnow=sync_time)
        result['data']['stock'] = base.get_stock_items(
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
                            base.mark_stock_item_synced(sync_id)
        base.update_last_sync(sync_time)
        sync_summary = {"synced_up": synced_up, "synced_down": synced}
        sync_msg = handle_sync_result(sync_summary)
        with open(dbdetails.path + '/log.txt', 'a') as f:
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

        redirect_target = request.args.get('redirect', False)
        if not redirect_target:
            return jsonify(sync_summary)
        else:
            return redirect(str(redirect_target) + "?msg=" + sync_msg)

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
            and not sync_summary['synced_up']['edited']['shift']
            and not sync_summary['synced_down']['deleted']['stock']
            and not sync_summary['synced_down']['added']['stock']
            and not sync_summary['synced_down']['edited']['stock']
            and not sync_summary['synced_up']['deleted']['stock']
            and not sync_summary['synced_up']['added']['stock']
            and not sync_summary['synced_up']['edited']['stock']):
        return "Nothing to sync"
    else:
        return "Sync done"

def insert_item(base, _type, item, sync_time):
    status = 0 if dbdetails.server else 3
    status = 2 if item['status'] == 2 else status
    if _type == "purchase":
        base.insert_purchase(item['country'], item['card'], item['date'],
                item['discount'], item['cart'], sync_time,
                location=item['location'], status=status,
                syncId=item['syncId'], note=item['note'])
    elif _type == "shift":
        base.insert_shift(item['workerId'], item['start'], item['end'],
                sync_time, location=item['location'], status=status,
                syncId=item['syncId'])
    elif _type == "stock":
        base.insert_stock_item(item['containerId'],
                item['quantity'], item['recounted'], item['edited'],
                location=item['location'], status=status,
                syncId=item['syncId']
        )


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
        pass # it is not possible to edit a stock item


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
        if dbdetails.server:
            base.mark_stock_item_deleted(sync_id)
        else:
            base.delete_stock_item(sync_id)


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
