#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable() # Displays any errors

from collections import OrderedDict
from datetime import datetime

import util
from dbconn import CgBase
from dbdetails import dbdetails

from flask import Blueprint, render_template, request, make_response

shifts_page = Blueprint('shifts_page', __name__,
        template_folder='templates')


@shifts_page.route('/shifts')
def shifts():
    # get/post and cookie
    msg = request.args.get('msg', None)
    new_cookies = {}
    location_cookie, location = util.get_location()
    if not location_cookie:
        new_cookies = {"location": str(location)}
    # data
    now = datetime.now()
    base = CgBase(location)
    stock = base.get_stock()
    workers = base.get_workers()
    version = base.get_version()
    workdays = [
            {"date": datetime.now(), "shifts": [
                {"workerId": 0, "duration": "5h", "status": 0},
                {"workerId": 4, "duration": "2h", "status": 3}
            ]},
            {"date": datetime(2016, 8, 12), "shifts": [
                {"workerId": 1, "duration": "1h", "status": 0},
                {"workerId": 3, "duration": "3h", "status": 3}
            ]}
    ]

    resp = make_response(render_template('shifts.html',
        title='Shifts',
        date=now,
        countries=util.country_list.items(),
        server=dbdetails.server,
        msg=msg,
        location=location,
        locations=util.locations,
        workers=workers,
        workdays=workdays,
        month="Agosto",
        version=version
    ))
    for key, val in new_cookies.iteritems():
        resp.set_cookie(key, val)
    return resp
