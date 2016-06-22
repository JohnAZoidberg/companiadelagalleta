#!/usr/bin/python -u
# coding=utf-8
import MySQLdb
from dbdetails import *

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

    def fetchone(self, table, columns, extra=""):
        self.cur.execute("SELECT " + self._list_to_str(columns) + " FROM " + table + " " + extra)
        result = self.cur.fetchone()
        return None if result is None else result[0]

    def fetchall(self, table, columns, extra=""):
        self.cur.execute("SELECT " + self._list_to_str(columns) + " FROM " + table + " " + extra)
        return self.cur.fetchall()

    def insert(self, table, columns, data, extra=""):
    # type: (str, List[obj], List[obj], str) -> None
        column_str = self._list_to_str(columns)
        data_str = self._list_to_str(data, '"')
        try:
            self.cur.execute("INSERT INTO " + table + " (" + column_str + ") VALUES (" + data_str + ") " + extra)
            self.cur.execute("SELECT LAST_INSERT_ID()")
            id = self.cur.fetchone()
            self.db.commit()
            return id
        except Exception as e:
            print "Something weird happened: ", e 
            self.db.rollback()
            return None

    def insert_purchase(self, country, card, date, discount, cart):
    # type: (str, bool, datetime, int, {int: int}) -> None
        cartId = self.fetchone("cart", ["cartId"], " ORDER BY cartId DESC")
        cartId = 0 if cartId is None else int(cartId) + 1
        for boxId, quantity in cart.iteritems():
            price = self.fetchone("boxes", ["price"], " WHERE boxesEntryId = " + str(boxId))
            if price is None:
                print "This boxId does not exist"
            # if discount == 10 then multiply by .9
            price = int(price * ((100 - discount) / 100.0)) 
            self.insert("cart",
                        ["cartId", "boxId", "quantity", "price"],
                        [cartId, boxId, quantity, price]) 
        self.insert("purchases",
                    ["country", "card", "date", "discount", "cartId"],
                    [country, int(card), self.sqlformatdate(date), discount, cartId])

    def get_purchases(self):
        pt = "purchases"
        ct = "cart"
        bt = "boxes"
        result = self.fetchall(pt+", "+ct+", "+bt,
                               [pt+".purchaseEntryId", pt+".country", pt+".card", pt+".discount", pt+".date",
                                ct+".quantity", ct+".price",
                                bt+".boxesEntryId", bt+".title"],
                               "WHERE purchases.cartId = cart.cartId AND boxes.boxesEntryId = cart.boxId ORDER BY " + pt +".date DESC")
        purchases = {}
        for row in result:
            (purchaseId, country, card, discount, date, quantity, price, boxId, title) = row
            key = int(row[0])
            try:
                foo = purchases[key]
            except:
                purchases[key] = {}
                purchases[key]['purchase'] = (country, card, discount, date)
                purchases[key]['cart'] = [] 
            purchases[key]['cart'].append((title, boxId, quantity, price))
        return purchases

