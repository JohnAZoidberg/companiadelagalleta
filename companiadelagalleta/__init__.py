#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from inspect import getmembers, isfunction

import util
from home import home_page
from stock import stock_page
from shifts import shifts_page
from update import update_page
from stats import stats_download
from api import api_page
from login import login_page, User
import jinja_filters
import jinja_tests
from dbdetails import dbdetails

from flask import Flask, g
from flask_login import LoginManager, session
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = dbdetails.secret

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page.login'
login_manager.session_protection = "strong"

app.config['MAIL_DEFAULT_SENDER'] = "galletas@danielschaefer.me"
app.config['MAIL_SERVER'] = 'smtp.strato.de'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'galletas@danielschaefer.me'
app.config['MAIL_PASSWORD'] = dbdetails.email_pw
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.before_request
def load_session_user():
    g.mail = mail
    if "user_id" in session:
        user = User.get(session["user_id"])
    else:
        user = User.get("anon")

    g.user = user

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
    app.run(debug=True, threaded=True)
