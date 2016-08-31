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
from flask_login import login_required

shifts_page = Blueprint('shifts_page', __name__,
        template_folder='templates')


@shifts_page.route('/shifts')
@login_required
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
    workers = base.get_workers()
    version = base.get_version()
    workdays, shift_totals = base.get_shift_stats()

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
        shift_totals=shift_totals,
        month="Agosto",
        version=version
    ))
    for key, val in new_cookies.iteritems():
        resp.set_cookie(key, val)
    return resp
