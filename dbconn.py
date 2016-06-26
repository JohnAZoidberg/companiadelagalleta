#!/usr/bin/python -u
# coding=utf-8
import MySQLdb
from dbdetails import *
from random import randint
import time
from collections import OrderedDict

class CgBase:
    def __init__(self):
        self.db = self._connectDb()
        self.cur = self.db.cursor()

    def _connectDb(self):
        return MySQLdb.connect(host=dbdetails.host,
                             user=dbdetails.user,
                             passwd=dbdetails.passwd,
                             db=dbdetails.db)
    def close_connection(self):
        self.db.close()

    def _list_to_str(self, xs, quote=""):
        str_value = quote + str(xs[0]) + quote 
        for x in xs[1:]:
            str_value += ", " + quote + str(x) + quote
        return str_value

    def sqlformatdate(self, date):
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def _fetch(self, table, columns, extra=""):
        try:
            self.cur.execute("SELECT " + self._list_to_str(columns) + " FROM " + table + " " + extra)
        except Exception as e:
            print "Something weird happened: ", e

    def fetchone(self, table, columns, extra=""):
        self._fetch(table, columns, extra)
        result = self.cur.fetchone()
        return None if result is None else result[0]

    def fetchall(self, table, columns, extra=""):
        self._fetch(table, columns, extra)
        return self.cur.fetchall()

    def insert(self, table, columns, data, commit, extra=""):
    # type: (str, List[obj], List[obj], str) -> None
        column_str = self._list_to_str(columns)
        data_str = self._list_to_str(data, '"')
        try:
            self.cur.execute("INSERT INTO " + table + " (" + column_str + ") VALUES (" + data_str + ") " + extra)
            self.cur.execute("SELECT LAST_INSERT_ID()")
            id = self.cur.fetchone()
            if commit:
                self.db.commit()
            return id
        except Exception as e:
            print "Something weird happened: ", e 
            self.db.rollback()
            return False 

    def insert_cart(self, syncId, boxId, quantity, price):
        return self.insert("cart",
                    ["syncId", "boxId", "quantity", "price"],
                    [syncId, boxId, quantity, price],
                    True)

    def insert_purchase(self, country, card, date, discount, cart, syncId=None):
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
            success = self.insert("cart",
                        ["boxId", "quantity", "price", "status", "syncId"],
                        [boxId, quantity, price, 0, syncId],
                        False)
        success = success and self.insert("purchases",
                    ["country", "card", "date", "discount", "status", "syncId"],
                    [country, int(card), self.sqlformatdate(date), discount, 0, syncId],
                    False)
        if success:
            self.db.commit()
        else:
            self.db.rollback() 

    def get_purchases(self):
        pt = "purchases"
        ct = "cart"
        bt = "boxes"
        result = self.fetchall(pt+", "+ct+", "+bt,
                               [pt+".syncId", pt+".country", pt+".card", pt+".discount", pt+".date", pt+".status",
                                ct+".quantity", ct+".price", ct+".status",
                                bt+".boxesEntryId", bt+".title"],
                               "WHERE purchases.syncId = cart.syncId AND boxes.boxesEntryId = cart.boxId ORDER BY " + pt +".date DESC")
        purchases = OrderedDict()
        for row in result:
            (syncId, country, card, discount, date, p_status, quantity, price, c_status, boxId, title) = row
            key = int(syncId)
            try:
                foo = purchases[key]
            except:
                purchases[key] = {}
                purchases[key]['purchase'] = (key, p_status, country, card, discount, date)
                purchases[key]['cart'] = [] 
            purchases[key]['cart'].append((title, c_status, boxId, quantity, price))
        return [val for key, val in purchases.iteritems()]

    def delete_purchase(self, syncId):
        syncStr = str(syncId)
        try:
            self.cur.execute("DELETE FROM purchases WHERE syncId = " + syncStr)
            self.cur.execute("DELETE FROM cart WHERE syncId = " + syncStr)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print "Someting weird happened: ", e
        return True

    def sync_cart(self, syncId, status, boxId, quantity, price):
        if status == 0:
            result = self.fetchone("cart", ["syncId"], "WHERE syncId="+str(syncId) + " AND boxId=" + str(boxId))
            if result is None:
                self.insert_cart(syncId, boxId, quantity, price)
        elif status == 1: # edited entry
            pass
        elif status == 2: # deleted entry 
            pass
        elif status == 3: # synced entry 
            pass
        return False

    def sync_purchase(self, syncId, status, country, card, discount, date):
        if status == 0: # new entry
            result = self.fetchone("purchases", ["status"], "WHERE syncId="+str(syncId))
            if result is None:
                self.insert_purchase(country, card, date, discount, {}, syncId=syncId)
                return True
        elif status == 1: # edited entry
            pass
        elif status == 2: # deleted entry 
            pass
        elif status == 3: # synced entry 
            pass
        return False
