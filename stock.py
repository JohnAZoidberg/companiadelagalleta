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

from flask import Blueprint, render_template, request

stock_page = Blueprint('stock_page', __name__, template_folder='templates')
@stock_page.route('/stock')
def stock():
    # temp
    msg = request.args.get('msg', None)
    location_cookie, location = util.get_location()
    if not location_cookie:
        new_cookies = {"location": str(location)}
    # data
    now = datetime.now()
    base = CgBase(location)
    stock = base.get_stock(returndict=True, containerIndexed=True)
    workers = base.get_workers()
    version = base.get_version()

    return render_template('stock.html',
        title='Stock',
        date=now,
        countries=util.country_list.items(),
        msg=msg,
        server=dbdetails.server,
        location=location,
        locations=util.locations,
        workers=workers,
        containers=util.containers,
        stock=stock,
        version=version
    )
