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
import json

import util
from dbconn import CgBase
from datetime import datetime

def print_html():
    # cgi
    form = cgi.FieldStorage()
    showndate = form.getfirst("date")
    msg = form.getfirst("msg")
    if msg is not None:
        msg = msg.replace("\n", "<br>")
    location = form.getfirst("location")
    # cookies
    cookies = util.get_cookies()
    new_cookies = {}
    if location is None:
        try:
            location = int(cookies['location'])
        except:
            location = 0
            new_cookies = {"location": location}
    else:
        location = int(location)
        new_cookies = {"location": location}
    # data
    now = datetime.now() if showndate is None else datetime.strptime(showndate, '%Y-%m-%d')
    base = CgBase(location)
    stock = base.get_stock(returndict=True, containerIndexed=True)
    workers = base.get_workers()
    version = base.get_version()

    # env
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True, lstrip_blocks=True)
    j2_env.filters['dateformat'] = util.dateformat
    j2_env.filters['datetimeformat'] = util.datetimeformat
    j2_env.filters['timeformat'] = util.timeformat
    j2_env.filters['moneyformat'] = util.moneyformat
    j2_env.filters['countryformat'] = util.countryformat
    j2_env.filters['cardformat'] = util.cardformat
    j2_env.filters['discountformat'] = util.discountformat
    j2_env.filters['adddays'] = util.adddays
    j2_env.filters['uniqueId'] = util.uniqueId
    j2_env.filters['json'] = json.dumps
    j2_env.filters['readable_version'] = util.readable_version
    j2_env.tests['continent'] = util.is_continent
    j2_env.tests['today'] = util.is_today

    # printing
    util.print_header(cookies=new_cookies)
    print j2_env.get_template('/templates/stock.html').render(
        title='Stock',
        date=now,
        location=location,
        locations=util.locations,
        workers=workers,
        containers=util.containers,
        stock=stock,
        version=version
    )

if __name__ == "__main__":
    print_html()
