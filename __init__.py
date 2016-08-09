#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from datetime import datetime
from inspect import getmembers, isfunction
import json

from dbconn import CgBase
import util
from dbdetails import dbdetails
import jinja_filters
import jinja_tests

from flask import Flask, render_template

app = Flask(__name__)
# add filters with inspection
my_filters = {name: function
                  for name, function in getmembers(jinja_filters)
                  if isfunction(function)}
app.jinja_env.filters['uniqueId'] = util.uniqueId
app.jinja_env.filters['json'] = json.dumps
app.jinja_env.filters.update(my_filters)

my_tests = {name: function
                  for name, function in getmembers(jinja_tests)
                  if isfunction(function)}

app.jinja_env.tests.update(my_tests)


@app.route('/')
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

if __name__ == "__main__":
    app.run(debug=True)
