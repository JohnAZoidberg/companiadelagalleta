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

from flask import Blueprint, render_template, request, make_response, g, flash, redirect, url_for, abort
from flask_login import login_required

shifts_page = Blueprint('shifts_page', __name__,
        template_folder='templates')


@shifts_page.route('/shifts')
@login_required
def shifts():
    if not g.user.admin:
        flash("The requested page is only accessible by admins!", "danger")
        return redirect(url_for("home_page.home"))
    # get/post and cookie
    new_cookies = {}
    location_cookie, location = util.get_location()
    if not location_cookie:
        new_cookies = {"location": str(location)}
    # data
    now = datetime.now()
    base = CgBase(location)
    workers = base.get_workers()
    version = base.get_version()
    workdays, shift_totals = base.get_shift_stats()

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
        month="Agosto",
        version=version
    ))
    for key, val in new_cookies.iteritems():
        resp.set_cookie(key, val)
    return resp


@shifts_page.route('/shifts/table')
@login_required
def shifts_table():
    if not g.user.admin:
        abort(401)
    # get/post and cookie
    showndate = request.args.get('date', None)
    location_cookie, location = util.get_location()
    # data
    now = datetime.now() if showndate is None\
          else datetime.strptime(showndate, '%Y-%m-%d')
    base = CgBase(location)
    workdays, shift_totals = base.get_shift_stats()

    return render_template('shifts_table.html',
        date=now,
        server=dbdetails.server,
        shift_totals=shift_totals,
        workdays=workdays,
        month="Agosto",
    )
