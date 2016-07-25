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

def perform_updates():
    util.print_header()
    if not util.checkConnection():
        print "No internet connection!"
        exit()

    # update git
    gitupdatestr = update.git_update()

    # update db
    reload(update)
    updatemsg = update.db_update()

    if not dbdetails.server:
        success, syncstr = api.sync()
        with open('log.txt', 'a') as f:
            f.writelines('\n'.join([
                    util.datetimeformat(datetime.now()),
                    str(gitupdatestr),
                    str(updatemsg),
                    str((success, syncstr)),
                    "-----\n"
            ]))
            print "written"
    return success

if __name__ == "__main__":
    if perform_updates():
        print "Location: index.py"
