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

from flask import Blueprint, render_template

home_page = Blueprint('home_page', __name__, template_folder='templates')
@home_page.route('/')
def home():
    # temp
    showndate = None
    location = 0
    msg = None
    # data
    now = datetime.now() if showndate is None\
          else datetime.strptime(showndate, '%Y-%m-%d')
    base = CgBase(location)
    boxes = base.get_boxes()
    purchases, total = util.calc_purchases_totals(
        base.get_purchases(onlydate=now, prettydict=True))
    workers = base.get_workers()
    version = base.get_version()
    return render_template('form.html',
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
    )
