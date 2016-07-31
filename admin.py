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
import urllib

def perform_updates():
    if not util.checkConnection():
        return "No internet connection!"

    # update git
    gitupdatestr = update.git_update()

    # update db
    reload(update)
    updatemsg = update.db_update()

    if not dbdetails.server:
        success, syncstr = api.sync()
        sync_json = syncstr
        if not sync_json['purchases']['synced_down']['deleted']\
           and not sync_json['purchases']['synced_down']['added']\
           and not sync_json['purchases']['synced_up']['deleted']\
           and not sync_json['purchases']['synced_up']['added']\
           and not sync_json['shifts']['synced_down']['deleted']\
           and not sync_json['shifts']['synced_down']['added']\
           and not sync_json['shifts']['synced_up']['deleted']\
           and not sync_json['shifts']['synced_up']['added']:
               updatemsg += "\nNothing to sync"
        elif success:
            updatemsg += "\nSync done"
        else:
            updatemsg += "\nSync problem!!!"

    else:
        success = True
        syncstr = "Server -> no sync"
    with open('log.txt', 'a') as f:
        f.writelines('\n'.join([
                util.datetimeformat(datetime.now()),
                "gitupdate:",
                str(gitupdatestr),
                "updatemsg",
                str(updatemsg),
                "sync",
                str((success, syncstr)),
                "-----\n"
        ]))
    return updatemsg

if __name__ == "__main__":
    msg = perform_updates()
    msg = urllib.quote(msg, safe='')
    print "Location: index.py?msg="+msg
    print
