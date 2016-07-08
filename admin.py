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
import api
from dbdetails import dbdetails
import update

def print_html():
    util.print_header()
    # update git
    try:
        gitupdatestr = update.git_update()
    except:
        util.print_header()
        print "Error"
        update.git_update()
    if not gitupdatestr == "Already up-to-date.\n":
        print "Location: admin.py"
        exit()

    util.print_header()
    print "Updates:", util.br
    # update db
    update.db_update()

    if not dbdetails.server:
        success, syncstr = api.sync()
        print util.br, "Sync:", util.br, syncstr

if __name__ == "__main__":
    print_html()
