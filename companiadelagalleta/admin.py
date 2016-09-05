#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable() # Displays any errors

from datetime import datetime
import urllib

import util
import api
from dbdetails import dbdetails
import update


def perform_updates():
    if not util.checkConnection():
        return "No internet connection!"

    # update git
    shell_success, shell_updatestr = update.git_update()

    if not shell_success:
        util.print_header()
        print "SHELL UPDATE ERROR: ", util.br
        print shell_updatestr
        exit()
    # update db
    reload(update)
    updatemsg = update.db_update()

    with open('log.txt', 'a') as f:
        f.writelines('\n'.join([
            util.datetimeformat(datetime.now()),
            "shellupdate:",
            str(shell_updatestr),
            "updatemsg",
            str(updatemsg),
            "-----\n"
        ]))
    return updatemsg

if __name__ == "__main__":
    msg = perform_updates()
    msg = urllib.quote(msg, safe='')
    print "Location: index.py?msg="+msg
    print
