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
import checkUpdate

def print_html():
    # cgi
    form = cgi.FieldStorage()
    action = form.getfirst("action")

    # data
    base = CgBase()

    # printing
    util.print_header()

    updatestr = checkUpdate.update()
    print "Updates:", util.br, updatestr, util.br
    success, syncstr = api.sync()
    print "Sync:", util.br, syncstr

if __name__ == "__main__":
    print_html()
