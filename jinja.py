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
from datetime import datetime

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def print_html():
    # data
    now = datetime.now()
    base = CgBase()
    boxes = base.get_boxes()
    purchases, card_total, cash_total = util.calc_purchases_totals(base.get_purchases(onlydate=now, prettydict=True))

    # env
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    j2_env.filters['dateformat'] = util.dateformat
    j2_env.filters['timeformat'] = util.timeformat
    j2_env.filters['moneyformat'] = util.moneyformat
    j2_env.filters['countryformat'] = util.countryformat
    j2_env.filters['cardformat'] = util.cardformat

    # printing
    util.print_header()
    print j2_env.get_template('/templates/form.html').render(
        title='Herramienta',
        date=now,
        countries=util.country_list.items(),
        boxes=boxes.items(),
        purchases=purchases,
        card_total=card_total,
        cash_total=cash_total
    )

if __name__ == "__main__":
    print_html()
