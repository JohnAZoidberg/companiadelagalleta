#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()

from datetime import datetime
import os

from dbconn import CgBase
import util

from openpyxl import load_workbook
from flask import Blueprint, send_from_directory, current_app as app

stats_download = Blueprint('stats_download', __name__)


@stats_download.route('/stats')
@util.only_admins(redirect_home=True)
def stats():
    create_stats_file(util.get_location()[1])
    return send_from_directory('', 'estadisticas.xlsx')


def colnum_string(n):
    div = n
    string = ""
    while div > 0:
        module = (div-1) % 26
        string = chr(65+module) + string
        div = int((div-module) / 26)
    return string


def day_to_datetime(day):
    return util.utc_strptime(day, '%Y-%m-%d')


def create_stats_file(location):
    base = CgBase(location)
    purchases = base.get_purchases(allLocations=True,
                                   newerthan=datetime(2016, 8, 1, 0, 0))
    boxes = base.get_boxes()
    # shifts = base.get_shifts(allLocations=True)

    # Insert sales
    wb = load_workbook(os.path.join(app.root_path, 'stats.xlsx'))
    ventas = wb.get_sheet_by_name("Ventas")
    old_entries = 553  # the number of entries in june and july
    for i, p in enumerate(reversed(purchases)):
        row = str(i + old_entries)
        cart = p['cart']
        ventas["A" + row] = p['date']
        ventas["B" + row] = util.country_list[p['country']]
        ventas["C" + row] = p['discount']
        ventas["D" + row] = p['card']
        ventas["G" + row] = p['note']
        total_price = 0
        total_boxes = 0
        for item in cart:
            col = 7 + item['boxId']
            quantity = item['quantity']
            total_price += quantity * item['price']
            total_boxes += quantity
            ventas[colnum_string(col) + row] = quantity
        ventas['E' + row] = total_boxes
        ventas['F' + row] = total_price / 10000.0

    # Insert boxes
    cajas = wb.get_sheet_by_name("Cajas")
    for boxId, box in boxes.iteritems():
        row = str(boxId+1)
        title = box['title']
        price = box['price'] / 10000.0
        cajas["A" + row] = boxId
        cajas["B" + row] = title
        cajas["C" + row] = price

    """# Insert work hours
    trabajo = wb.get_sheet_by_name("Trabajo")
    row = 2
    for item in shifts:
        s_row = str(row)
        trabajo["A" + s_row] = util.all_workers[item['workerId']]
        trabajo["B" + s_row] = item['start']
        trabajo["C" + s_row] = item['end']
        row += 1"""

    wb.save(os.path.join(app.root_path, 'estadisticas.xlsx'))
