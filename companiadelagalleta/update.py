#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

import subprocess
import os

import jinja_filters
from dbconn import CgBase
import util

from flask import Blueprint, redirect, flash, url_for, current_app as app
from flask_login import login_required


update_page = Blueprint('update_page', __name__, template_folder='templates')

@update_page.route('/update', methods=['GET'])
@util.only_admins(redirect_home=True)
def update():
    success, git_msg = git_update()
    util.log(git_msg)
    if success:
        if "Already up-to-date.\n" in git_msg:
            flash("Already up-to-date.", 'info')
        else:
            flash("Successfully updated.", 'info')
        return redirect(url_for("update_page.update_db"))
    else:
        flash("Problem during updating!! Please report to Daniel", 'danger')
        return redirect(url_for("home_page.home"))


@update_page.route('/update/git', methods=['GET'])
@util.only_admins(redirect_home=True)
def update_git():
    success, git_msg = git_update()
    util.log(git_msg)
    if success:
        if "Already up-to-date.\n" in git_msg:
            flash("Already up-to-date.", 'info')
        else:
            flash("Successfully updated.", 'info')
        return redirect(url_for("home_page.home"))
    else:
        flash("Problem during updating!! Please report to Daniel", 'danger')
        return redirect(url_for("home_page.home"))

@update_page.route('/update/db', methods=['GET'])
@util.only_admins(redirect_home=True)
def update_db():
    update_msg = db_update()
    util.log(update_msg)
    flash(update_msg, 'info')
    return redirect(url_for("home_page.home"))


def git_update():
    process = subprocess.Popen(
        [os.path.join(app.root_path, "update.sh"), app.root_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    returncode = process.wait()
    return [returncode == 0, process.stdout.read()]


def db_update():
    result = ""
    base = CgBase(0)
    version = 0
    new_version = None
    failure = False
    try:
        version = base.get_version()
    except Exception as e:
        if str(e) == "(1146, \"Table 'cg.config' doesn't exist\")" or\
                str(e) == "(1146, \"Table 'beta.config' doesn't exist\")":
            version = 0  # 0.0.0
            sql = (
                  "CREATE TABLE config ("
                  "constant CHAR(1) DEFAULT 'X' NOT NULL PRIMARY KEY,"
                  "CHECK (constant = 'X'),"
                  "version int DEFAULT 10 NOT NULL,"
                  "last_sync datetime DEFAULT '2016-01-01 00:00:00' NOT NULL"
                  ")"
            )
            base.cur.execute(sql)
            base.cur.execute("INSERT INTO config () VALUES ()")
            base.db.commit()
    if version < 10004:
        result += "Add option to remove and add shifts\n"
        new_version = 10004  # 1.0.4
    if version < 10100:
        try:
            # set db timezone to UTC
            base.cur.execute("SET @@global.time_zone='+00:00'")
            # update all entries to UTC
            tables = [
                ("config", "last_sync"),
                ("purchases", "date"),
                ("purchases", "edited"),
                ("shifts", "start"),
                ("shifts", "end"),
                ("shifts", "edited"),
                ("stock", "date"),
                ("stock", "edited")
            ]
            for table, column in tables:
                base.cur.execute(
                    "UPDATE {0} SET {1} = {1} - INTERVAL 1 HOUR"
                    .format(table, column))

            base.db.commit()

            result += "Make dates and times timezone agnostic\n"
            new_version = 10100  # 1.1.0
        except:
            base.db.rollback()
            raise

    if new_version is not None:
        if not failure:
            base.update("config",
                        {"version": new_version}, True,
                        ("WHERE constant = 'X'", ()))
            base.db.commit()
            result += ("Updated from " + jinja_filters.readable_version(version)
                    + " to " + jinja_filters.readable_version(new_version)+"\n")
        else:
            base.db.rollback()
            result += "FAILURE!\n"
    else:
        result += "No update available("+jinja_filters.readable_version(version)+")\n"
    return result

if __name__ == "__main__":
    util.print_header()
    #print db_update()
    print git_update()
