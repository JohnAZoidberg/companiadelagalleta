#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from inspect import getmembers, isfunction

import util
from dbdetails import dbdetails as dbd
from home import home_page
from stock import stock_page
from shifts import shifts_page
from update import update_page
from stats import stats_download
from api import api_page
from login import login_page, User
import jinja_filters
import jinja_tests
from models import db

from flask import Flask, g
from flask_login import LoginManager, session

app = Flask(__name__)
db_uri = 'mysql://{}:{}@{}/{}'.format(dbd.user, dbd.passwd, dbd.host, "alchemy")
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page.login'
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.before_request
def load_session_user():
    if "user_id" in session:
        user = User.get(session["user_id"])
    else:
        user = User.get("anon")

    g.user = user

@app.before_first_request
def create_database():
     db.create_all()

# add jinja filters and testswith inspection
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
app.register_blueprint(stock_page)
app.register_blueprint(shifts_page)
app.register_blueprint(update_page)
app.register_blueprint(api_page)
app.register_blueprint(login_page)
app.register_blueprint(stats_download)


if __name__ == "__main__":
    from dbdetails import dbdetails
    app.config['SECRET_KEY'] = dbdetails.secret
    app.run(debug=True, threaded=True)
