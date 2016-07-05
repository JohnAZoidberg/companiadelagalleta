#!/usr/bin/python -u
# coding=utf-8
import MySQLdb
from dbdetails import *
from random import randint
import time
from collections import OrderedDict
from datetime import datetime
import util

class CgBase:
    def __init__(self):
        self.db = self._connectDb()
        self.cur = self.db.cursor()

    def _connectDb(self):
        return MySQLdb.connect(host=dbdetails.host,
                             user=dbdetails.user,
                             passwd=dbdetails.passwd,
                             db=dbdetails.db,
                             use_unicode=True,
                             charset='utf8')
    def close_connection(self):
        self.db.close()

    def _list_to_str(self, xs, quote=""):
        str_value = quote + str(xs[0]) + quote 
        for x in xs[1:]:
            str_value += ", " + quote + str(x) + quote
        return str_value

    def _fetch(self, table, columns, extra=""):
        try:
            self.cur.execute("SELECT " + self._list_to_str(columns) + " FROM " + table + " " + extra)
        except:
            raise

    def fetchone(self, table, columns, extra=""):
        self._fetch(table, columns, extra)
        result = self.cur.fetchone()
        return None if result is None else result[0]

    def fetchall(self, table, columns, extra=""):
        self._fetch(table, columns, extra)
        return self.cur.fetchall()

    def update(self, table, columnsdata, commit, extra):
        try:
            first = True
            sqlstr = "UPDATE " + table + " SET "
            for col, d in columnsdata.iteritems():
                if not first:
                    sqlstr += ", "
                sqlstr += str(col) + ' = "' + str(d) + '"'
                first = False
            sqlstr += " " + extra
            self.cur.execute(sqlstr)
            if commit:
                self.db.commit()
            return True
        except:
            self.db.rollback()
            raise
        return False

    def insert(self, table, columns_data, commit, extra=""):
    # type: (str, {obj: obj}, str) -> None
        column_str = self._list_to_str(columns_data.keys())
        data_str = self._list_to_str(columns_data.values(), '"')
        try:
            self.cur.execute("INSERT INTO " + table + " (" + column_str + ") VALUES (" + data_str + ") " + extra)
            self.cur.execute("SELECT LAST_INSERT_ID()")
            id = self.cur.fetchone()
            if commit:
                self.db.commit()
            return id
        except:
            self.db.rollback()
            raise
            return False 

    def insert_purchase(self, country, card, date, discount, cart, edited, status=0, syncId=None):
    # type: (str, bool, datetime, int, {int: int}) -> None
        # a unique id to identify entries: unixtimestamp + 4 random digits
        success = False
        if syncId is None:
            syncId = str(randint(100000000, 999999999))
        if len(cart) == 0:
            success = True
        for boxId, quantity in cart.iteritems():
            price = self.fetchone("boxes", ["price"], " WHERE boxesEntryId = " + str(boxId))
            if price is None:
                print "This boxId does not exist"
            # if discount == 10 then multiply by .9
            price = int(price * ((100 - discount) / 100.0)) 
            # status: 0: new, 1: edited, 2: deleted, 3: synced
            success = self.insert("cart", {"syncId": syncId, "boxId": boxId, "quantity": quantity, "price": price}, False)
        success = success and self.insert("purchases",
                    {"country": country, "card": int(card), "date": util.datestring(date), "discount": discount, "status": status, "syncId": syncId, "edited": edited},
                    False)
        if success:
            self.db.commit()
        else:
            self.db.rollback() 
        return success

    def get_purchases(self, getDeleted=False, prettydict=False, onlydate=None, newerthan=None, datestring=False, notsynced=False):
        pt = "purchases"
        ct = "cart"
        bt = "boxes"
        result = self.fetchall(pt+", "+ct+", "+bt,
                               [pt+".syncId", pt+".country", pt+".card", pt+".discount", pt+".date", pt+".status", pt+".edited",
                                ct+".quantity", ct+".price",
                                bt+".boxesEntryId", bt+".title"],
                               "WHERE purchases.syncId = cart.syncId AND boxes.boxesEntryId = cart.boxId ORDER BY " + pt +".date DESC")
        purchases = OrderedDict()
        for row in result:
            (syncId, country, card, discount, date, status, edited, quantity, price, boxId, title) = row
            if onlydate is not None:
                if not util.is_same_day(onlydate, date):
                    continue
            if newerthan is not None:
                if newerthan > edited:
                    continue
            if notsynced and status == 3:
                continue
            if not getDeleted and status == 2:
                continue 
            if datestring:
                date = util.datestring(date)
                edited = util.datestring(edited)
            key = int(syncId)
            try:
                foo = purchases[key]
            except:
                purchases[key] = {}
                if prettydict:
                    purchases[key]['purchase'] = {"syncId": key, "status": status, "country": country, "card": card, "discount": discount, "date": date, "edited": edited} 
                else:
                    purchases[key]['purchase'] = (key, status, country, card, discount, date)
                purchases[key]['cart'] = [] 
            if prettydict:
                purchases[key]['cart'].append({"title": title, "boxId": boxId, "quantity": quantity, "price": price})
            else:
                purchases[key]['cart'].append((title, boxId, quantity, price))
        return [val for key, val in purchases.iteritems()]

    def mark_purchase_deleted(self, syncId):
        syncStr= str(syncId)
        success = self.update("purchases", {"status": 2}, False, "WHERE syncId="+syncStr)
        if success:
            self.db.commit()
        return success

    def delete_purchase(self, syncId):
        syncStr = str(syncId)
        try:
            self.cur.execute("DELETE FROM purchases WHERE syncId = " + syncStr)
            self.cur.execute("DELETE FROM cart WHERE syncId = " + syncStr)
            self.db.commit()
        except:
            self.db.rollback()
            raise
            return False
        return True

        def mark_synced(self, syncId, boxId):
        self.update("purchases", {"status": 3}, True, "WHERE syncId="+str(syncId))
        self.update("cart", {"status": 3}, True, "WHERE syncId="+str(syncId)+" AND boxId=" + str(boxId))

    def get_boxes(self):
        boxes = OrderedDict()
        results = self.fetchall("boxes", ["boxesEntryId", "title", "price"])
        for result in results:
            (boxId, title, price) = result
            boxes[boxId] = title
        return boxes

    def get_box_stats(self):
        stats = {} 
        results = self.fetchall("cart, purchases", 
                                ["cart.boxId", "cart.quantity", "purchases.date"],
                                "WHERE cart.syncId = purchases.syncId AND cart.status != 2 ORDER BY date ASC")
        for (boxId, quantity, date) in results:
            date = date.strftime('%Y-%m-%d')
            try:
                foo = stats[date]
            except:
                stats[date] = {}
            try:
                foo = stats[date][boxId] 
                stats[date][boxId] += quantity 
            except:
                stats[date][boxId] = quantity 
        return stats

    def update_last_sync(self, date):
        self.update("config", {"last_sync": util.datestring(date)}, False, "")
    
    def get_last_sync(self):
        return self.fetchone("config", ["last_sync"], "")
