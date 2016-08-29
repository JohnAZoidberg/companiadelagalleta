#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from collections import OrderedDict
from datetime import datetime

from dbconn import CgBase
import util
from dbdetails import dbdetails

from flask import Blueprint, render_template, request, make_response, jsonify

home_page = Blueprint('home_page', __name__, template_folder='templates')
@home_page.route('/', methods=['GET'])
@home_page.route('/home', methods=['GET'])
def home():
    # get/post and cookie
    showndate = request.args.get('date', None)
    msg = request.args.get('msg', None)
    new_cookies = {}
    location_cookie, location = util.get_location()
    if not location_cookie:
        new_cookies = {"location": str(location)}

    # data
    now = datetime.now() if showndate is None\
          else datetime.strptime(showndate, '%Y-%m-%d')
    base = CgBase(location)
    boxes = base.get_boxes()
    purchases, total = util.calc_purchases_totals(
        base.get_purchases(onlydate=now))
    workers = base.get_workers()
    version = base.get_version()

    resp = make_response(render_template('home.html',
        title='Herramienta',
        date=now,
        countries=util.country_list.items(),
        boxes=boxes.items(),
        purchases=purchases,
        total=total,
        msg=msg,
        server=dbdetails.server,
        workers=workers,
        location=location,
        locations=util.locations,
        version=version
    ))
    for key, val in new_cookies.iteritems():
        resp.set_cookie(key, val)
    return resp


@home_page.route('/hello', methods=['GET'])
def hello():
    return "Hello beautiful World"


@home_page.route('/test', methods=['GET'])
def test():
    base = CgBase(0)
    base.cur.execute((
        "SELECT workerId, c.boxId, c.quantity"
        " FROM shifts AS s, purchases AS p, cart AS c"
        " WHERE s.location = 0 AND s.status <> 2"
        " AND p.location = 0 AND p.status <> 2"
        " AND s.start < p.date AND p.date < s.end"
        " AND p.syncId = c.syncId"
        " ORDER BY c.boxID ASC"
    ))
    base.cur.execute((
        "SELECT workerId, SUM(TIMESTAMPDIFF(SECOND, start, end)) / 3600"
        " FROM shifts"
        " WHERE location = 0 AND status <> 2"
        " GROUP BY workerId"
    ))
    base.cur.execute((
        "SELECT workerId, DATE(start), start, end, TIMEDIFF(start, end)"
        " FROM shifts"
        " WHERE location = 0 AND status <> 2"
        " AND MONTH(start) = 8 AND YEAR(start) = 2016"
        " ORDER BY start DESC"
    ))
    result = base.cur.fetchall()
    workdays = OrderedDict()
    for row in result:
        (workerId, workdate, start, end, duration) = row
        shift = {
            "workerId": workerId,
            "worker": util.all_workers[workerId],
            "duration": duration
        }
        try:
            workdays[workdate].append(shift)
        except KeyError:
            workdays[workdate] = [shift]
    return str(workdays)

@home_page.route('/purchases', methods=['GET'])
def purchases():
    # get/post and cookie
    showndate = request.args.get('date', None)
    location_cookie, location = util.get_location()

    # data
    now = datetime.now() if showndate is None\
          else datetime.strptime(showndate, '%Y-%m-%d')
    base = CgBase(location)
    purchases, total = util.calc_purchases_totals(
        base.get_purchases(onlydate=now))

    return render_template('purchases.html',
        date=now,
        purchases=purchases,
        total=total,
        server=dbdetails.server,
        location=location,
    )
