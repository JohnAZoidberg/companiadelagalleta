#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from datetime import datetime

from dbconn import CgBase
import util
from dbdetails import dbdetails

from flask import Blueprint, render_template, request, make_response

home_page = Blueprint('home_page', __name__, template_folder='templates')
@home_page.route('/', methods=['GET'])
@home_page.route('/home', methods=['GET'])
def home():
    new_cookies = {}
    # get/post and cookie
    showndate = request.args.get('date', None)
    msg = request.args.get('msg', None)
    location_cookie, location = util.get_location()
    if not location_cookie:
        new_cookies = {"location": str(location)}

    # data
    now = datetime.now() if showndate is None\
          else datetime.strptime(showndate, '%Y-%m-%d')
    base = CgBase(location)
    boxes = base.get_boxes()
    purchases, total = util.calc_purchases_totals(
        base.get_purchases(onlydate=now, prettydict=True))
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
        base.get_purchases(onlydate=now, prettydict=True))

    return render_template('purchases.html',
        date=now,
        purchases=purchases,
        total=total,
        server=dbdetails.server,
        location=location,
    )
