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
    gitupdatestr = update.git_update()
    if gitupdatestr == "Already up-to-date.\n":
        gitupdatestr = ""
    else:
        gitupdatestr += util.br

    print "Updates:", util.br, gitupdatestr
    # update db
    reload(update)
    update.db_update()

    if not dbdetails.server:
        success, syncstr = api.sync()
        print util.br, "Sync:", util.br, syncstr

if __name__ == "__main__":
    print_html()
