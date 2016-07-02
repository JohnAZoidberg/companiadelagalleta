#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable() # Displays any errors

from jinja2 import Environment, FileSystemLoader
import os

import util
from dbconn import CgBase

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def print_html():
    base = CgBase()
    boxes = base.get_boxes()
    purchases = base.get_purchases()

    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    util.print_header()
    print j2_env.get_template('/templates/form.html').render(
        title='Hellow Gist from GutHub',
        now='18:04',
        countries=util.country_list.items(),
        boxes=boxes.items(),
        purchases=purchases
    )

if __name__ == "__main__":
    print_html()
