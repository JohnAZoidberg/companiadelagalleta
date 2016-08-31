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

from flask import Blueprint, render_template, request, make_response, g, abort, flash, redirect, url_for
from flask_login import login_required

stock_page = Blueprint('stock_page', __name__, template_folder='templates')


@stock_page.route('/stock')
@login_required
def stock():
    if not g.user.admin:
        flash("The requested page is only accessible by admins!", "danger")
        return redirect(url_for("home_page.home"))
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

    resp = make_response(render_template('stock.html',
        title='Stock',
        date=now,
        countries=util.country_list.items(),
        server=dbdetails.server,
        msg=msg,
        location=location,
        locations=util.locations,
        workers=workers,
        containers=util.containers,
        stock=stock,
        version=version
    ))
    for key, val in new_cookies.iteritems():
        resp.set_cookie(key, val)
    return resp


@stock_page.route('/stock/form')
@login_required
def stock_form():
    if not g.user.admin:
        abort(401)
    # get/post and cookie
    location_cookie, location = util.get_location()
    # data
    base = CgBase(location)
    stock = base.get_stock()

    return render_template('stock_form.html',
        containers=util.containers,
        stock=stock
    )
