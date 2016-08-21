#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()

from datetime import datetime

from dbconn import CgBase
import util
from dbdetails import dbdetails

from openpyxl import load_workbook
from flask import Blueprint, render_template, request, make_response, redirect, send_from_directory

stats_download = Blueprint('stats_download', __name__)
@stats_download.route('/stats')
def stats():
    create_stats_file()
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
    return datetime.strptime(day, '%Y-%m-%d')


def create_stats_file():
    base = CgBase(util.get_location()[1])
    purchases = base.get_purchases(allLocations=True)
    boxes = base.get_boxes()

    wb = load_workbook(dbdetails.path + '/stats.xlsx')
    ventas = wb.get_sheet_by_name("Ventas")
    for i, p in enumerate(reversed(purchases)):
        row = str(i + 2)
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

    cajas = wb.get_sheet_by_name("Cajas")
    for boxId, box in boxes.iteritems():
        row = str(boxId+1)
        title = box['title']
        price = box['price'] / 10000.0
        cajas["A" + row] = boxId
        cajas["B" + row] = title
        cajas["C" + row] = price

    wb.save(dbdetails.path + "/estadisticas.xlsx")
