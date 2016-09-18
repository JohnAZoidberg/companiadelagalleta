#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from datetime import datetime

from dbdetails import dbdetails
from dbconn import CgBase
import util

from flask import Blueprint, render_template, request, make_response,\
                  flash, redirect, url_for, g
from flask_login import UserMixin, login_user, logout_user

login_page = Blueprint('login_page', __name__, template_folder='templates')


@login_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
            return show_login()
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query_filter_by(username=username,
                                           password=password)
    if registered_user is None:
        flash('Username or Password is invalid', 'danger')
        return redirect(url_for('login_page.login'))
    login_user(registered_user)
    flash('Logged in successfully', 'info')
    return redirect(request.args.get('next') or url_for('home_page.home'))

@login_page.route('/logout')
def logout():
    flash('Logged out successfully', 'info')
    logout_user()
    return redirect(url_for('login_page.login'))

def show_login():
    if g.user.is_authenticated():
        return redirect(url_for('home_page.home'))
    # get/post and cookie
    new_cookies = {}
    location_cookie, location = util.get_location()
    if not location_cookie:
        new_cookies = {"location": str(location)}

    # data
    now = datetime.utcnow()
    base = CgBase(location)
    version = base.get_version()
    workers = base.get_workers()

    resp = make_response(render_template('login.html',
        title='Login',
        date=now,
        server=dbdetails.server,
        workers=workers,
        location=location,
        locations=util.locations,
        version=version
    ))
    for key, val in new_cookies.iteritems():
        resp.set_cookie(key, val)
    return resp

class User(UserMixin):
    # proxy for a database of users
    user_database = {
        "anon": ("anon", "anon", False),
        "tienda": ("tienda", "tienda", False),
        "Roberta": ("Roberta", "danidelverano", True),
        "zoid": ("zoid", "zoid", True)
    }

    def __init__(self, username, password, admin):
        self.id = username
        self.username = username
        self.password = password
        self.admin = admin

    def is_authenticated(self):
        return not self.is_anonymous()

    def is_anonymous(self):
        return self.username == "anon"

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_admin(self):
        return self.admin

    @classmethod
    def query_filter_by(cls, username=None, password=None):
        for id, (user, pwd, admin) in cls.user_database.iteritems():
            if user == username and pwd == password:
                return cls.get(id)
        return None

    @classmethod
    def get(cls, id):
        user = cls.user_database.get(id)
        return None if user is None else User(user[0], user[1], user[2])

    def __repr__(self):
        if self.admin:
            return '<Admin %r>' % self.username
        else:
            return '<User %r>' % self.username
