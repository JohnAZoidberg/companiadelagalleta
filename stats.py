#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()
import cgi
import json
from datetime import datetime
from dbconn import *
from random import randint
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import util
from openpyxl import load_workbook

def colnum_string(n):
    div = n
    string = ""
    temp = 0
    while div > 0:
        module = (div-1) % 26
        string = chr(65+module) + string
        div = int((div-module) / 26)
    return string

def day_to_datetime(day):
    return datetime.strptime(day, '%Y-%m-%d')

def create_stats_file():
    form = cgi.FieldStorage()
    base = CgBase()
    purchases = base.get_purchases(prettydict=True)
    boxes = base.get_boxes()

    wb = load_workbook('stats.xlsx')
    ventas = wb.get_sheet_by_name("Ventas")
    for i, p in enumerate(reversed(purchases)):
        row = str(i + 2)
        purchase = p['purchase']
        cart = p['cart']
        ventas["A" + row] = purchase['date']
        ventas["B" + row] = util.country_list[purchase['country']]
        ventas["C" + row] = purchase['discount']
        ventas["D" + row] = purchase['card']
        total_price = 0
        total_boxes = 0
        for item in cart:
            col = 6 + item['boxId']
            quantity = item['quantity']
            total_price += quantity * item['price']
            total_boxes += quantity
            ventas[colnum_string(col) + row] = quantity
        ventas['E' + row] = total_boxes
        ventas['F' + row] = total_price / 100.0

    cajas = wb.get_sheet_by_name("Cajas")
    for boxId, box in boxes.iteritems():
        row = str(boxId+1)
        title = box['title']
        price = box['price'] / 100.0
        cajas["A" + row] = boxId
        cajas["B" + row] = title
        cajas["C" + row] = price

    wb.save("estadisticas.xlsx")
    print "Location: estadisticas.xlsx\n"

if __name__ == "__main__":
    create_stats_file()
