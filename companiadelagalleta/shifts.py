#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable() # Displays any errors

from datetime import datetime

import util
from dbconn import CgBase
from dbdetails import dbdetails

from flask import Blueprint, render_template, request, make_response

shifts_page = Blueprint('shifts_page', __name__,
        template_folder='templates')

months = [
    (9, 2016),
    (8, 2016)
]

@shifts_page.route('/shifts')
@util.only_admins(redirect_home=True)
def shifts():
    now = datetime.utcnow()
    # get/post and cookie
    new_cookies = {}
    location_cookie, location = util.get_location()
    if not location_cookie:
        new_cookies = {"location": str(location)}
    month = int(request.args.get("month", now.month))
    year = int(request.args.get("year", now.year))
    # data
    base = CgBase(location)
    workers = base.get_workers()
    version = base.get_version()
    workdays, shift_totals = base.get_shift_stats(month, year)

    resp = make_response(render_template('shifts.html',
        title='Shifts',
        date=now,
        countries=util.country_list.items(),
        server=dbdetails.server,
        location=location,
        locations=util.locations,
        workers=workers,
        workdays=workdays,
        shift_totals=shift_totals,
        shown_month=month,
        shown_year=year,
        months=months,
        version=version
    ))
    for key, val in new_cookies.iteritems():
        resp.set_cookie(key, val)
    return resp


@shifts_page.route('/shifts/table')
@util.only_admins(redirect_home=False)
def shifts_table():
    now = datetime.utcnow()
    # get/post and cookie
    location_cookie, location = util.get_location()
    # data
    month = int(request.args.get("month", now.month))
    year = int(request.args.get("year", now.year))
    base = CgBase(location)
    workdays, shift_totals = base.get_shift_stats(month, year)

    return render_template('shifts_table.html',
        date=now,
        server=dbdetails.server,
        shift_totals=shift_totals,
        workdays=workdays,
        shown_month=month,
        shown_year=year,
        months=months
    )
