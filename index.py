#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable() # Displays any errors

from jinja2 import Environment, FileSystemLoader
import os
import cgi

import util
from dbconn import CgBase
from datetime import datetime
from dbdetails import *

def print_html():
    # cgi
    form = cgi.FieldStorage()
    showndate = form.getfirst("date")
    msg = form.getfirst("msg")
    if msg is not None:
        msg = msg.replace("\n", "<br>")
    # data
    now = datetime.now() if showndate is None else datetime.strptime(showndate, '%Y-%m-%d')
    base = CgBase()
    boxes = base.get_boxes()
    purchases, total = util.calc_purchases_totals(base.get_purchases(onlydate=now, prettydict=True))
    version = base.get_version()

    # env
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    j2_env.filters['dateformat'] = util.dateformat
    j2_env.filters['datetimeformat'] = util.datetimeformat
    j2_env.filters['timeformat'] = util.timeformat
    j2_env.filters['moneyformat'] = util.moneyformat
    j2_env.filters['countryformat'] = util.countryformat
    j2_env.filters['cardformat'] = util.cardformat
    j2_env.filters['discountformat'] = util.discountformat
    j2_env.filters['adddays'] = util.adddays
    j2_env.filters['uniqueId'] = util.uniqueId
    j2_env.tests['continent'] = util.is_continent
    j2_env.tests['today'] = util.is_today

    # printing
    util.print_header()
    print j2_env.get_template('/templates/form.html').render(
        title='Herramienta',
        date=now,
        countries=util.country_list.items(),
        boxes=boxes.items(),
        purchases=purchases,
        total=total,
        msg=msg,
        server=dbdetails.server,
        version=version
        #random_prefix=util.uniqueId()
    )

if __name__ == "__main__":
    print_html()
