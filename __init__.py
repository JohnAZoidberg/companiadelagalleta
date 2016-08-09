#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from datetime import datetime
from inspect import getmembers, isfunction

from dbconn import CgBase
import util
from dbdetails import dbdetails
from home import home_page
import jinja_filters
import jinja_tests

from flask import Flask, render_template

app = Flask(__name__)
# add filters with inspection
my_filters = {name: function
                  for name, function in getmembers(jinja_filters)
                  if isfunction(function)}
app.jinja_env.filters['uniqueId'] = util.uniqueId
app.jinja_env.filters.update(my_filters)

my_tests = {name: function
                  for name, function in getmembers(jinja_tests)
                  if isfunction(function)}

app.jinja_env.tests.update(my_tests)

# Remove unnecessary whitespace
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.register_blueprint(home_page)

if __name__ == "__main__":
    app.run(debug=True)
