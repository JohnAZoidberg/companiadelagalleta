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

def print_html():
    # cgi
    form = cgi.FieldStorage()
    location = form.getfirst("location")
    # cookies
    cookies = util.get_cookies()
    new_cookies = {}
    if location is None:
        try:
            location = int(cookies['location'])
        except:
            location = 0
            new_cookies = {"location": location}
    else:
        location = int(location)
        new_cookies = {"location": location}
    # data
    base = CgBase(location)
    stock = base.get_stock(returndict=True, containerIndexed=True)
    workers = base.get_workers()
    version = base.get_version()

    # env
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True, lstrip_blocks=True)
    j2_env.filters['readable_version'] = util.readable_version

    # printing
    util.print_header(cookies=new_cookies)
    print j2_env.get_template('/templates/stock.html').render(
        title='Stock',
        location=location,
        locations=util.locations,
        workers=workers,
        containers=util.containers,
        stock=stock,
        version=version
    )

if __name__ == "__main__":
    print_html()
