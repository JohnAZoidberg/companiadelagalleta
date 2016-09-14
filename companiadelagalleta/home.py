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
from model import *

from flask import Blueprint, render_template, request, make_response, g,\
    redirect, flash, url_for, jsonify
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
    purchases = [{"ps": Purchase.query.all(), "total": {"card": 0, "cash": 0}}]
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
    #base = CgBase(0)
    #util.log("Testlog")
    #meloneras = model.Location(0, "Meloneras")
    #strelitzia = model.Container(15, "Strelitzia")
    #strl_can = model.Box(52, "Strelitzia Sabores Canarias", 149500, 15)
    #strl_veg = model.Box(62, "Strelitzia Vegana", 159500, 15)
    #shift = model.Shift(0, 1, datetime.now())
    #strelitzia_stock = model.StockItem(0, 15, 5, 1, datetime.now())
    #carts = [
        #CartItem(None, 52, 1, 149500),
        #CartItem(None, 62, 2, 159500)
    #]
    #purchase = Purchase(0, "de", False, 0, datetime.now(), carts)
    #g.db.session.add(strelitzia)
    #g.db.session.add(strl_can)
    #g.db.session.add(strl_veg)
    #g.db.session.add(strelitzia_stock)
    #g.db.session.add(shift)
    #g.db.session.commit()
    #g.db.session.add(purchase)
    #g.db.session.commit()
    #res = model.Purchase.query.all()
    res = Box.query.get(10)
    print res
    res = Box.query.get("10")
    print res

    return "Queried"


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
