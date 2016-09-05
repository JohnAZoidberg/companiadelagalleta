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

from flask import Blueprint, render_template, request, make_response, g,\
    redirect, flash, url_for
from flask_login import login_required

home_page = Blueprint('home_page', __name__, template_folder='templates')
@home_page.route('/', methods=['GET'])
@home_page.route('/home', methods=['GET'])
@login_required
def home():
    # get/post and cookie
    showndate = request.args.get('date', None)
    new_cookies = {}
    location_cookie, location = util.get_location()
    if not location_cookie:
        new_cookies = {"location": str(location)}

    # date
    if showndate is None:
        now = datetime.now()
    elif g.user.is_admin():
        now = datetime.strptime(showndate, '%Y-%m-%d')
    else:
        flash("Only admins can view past dates!", "danger")
        return redirect(url_for("home_page.home"))
    # data
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
@util.only_admins(redirect_home=False)
def test():
    base = CgBase(0)
    #util.log("Testlog")
    return "Done"

@login_required
@home_page.route('/purchases', methods=['GET'])
def purchases():
    # get/post and cookie
    showndate = request.args.get('date', None)
    location_cookie, location = util.get_location()

    # date
    if showndate is None:
        now = datetime.now()
    elif g.user.is_admin():
        now = datetime.strptime(showndate, '%Y-%m-%d')
    else:
        flash("Only admins can view past dates!", "danger")
        return redirect(url_for("home_page.home"))

    # data
    base = CgBase(location)
    purchases, total = util.calc_purchases_totals(
        base.get_purchases(onlydate=now))

    return render_template('purchases.html',
        purchases=purchases,
        total=total,
        server=dbdetails.server,
        location=location,
    )
