#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from collections import OrderedDict
from datetime import datetime

import MySQLdb

import util
from dbdetails import dbdetails
import jinja_filters


class CgBase:
    def __init__(self, location):
        self.db = self._connectDb()
        self.cur = self.db.cursor()
        self.location = location

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

    def _list_to_sql(self, xs):
        str_value = "%s"
        for x in xs[1:]:
            """if x is None:
                str_value += ", NULL"
            else:"""
            str_value += ", %s"
        return str_value, tuple(xs)

    def _fetch(self, table, columns, extra=("", ())):
        try:
            self.cur.execute("SELECT " + self._list_to_str(columns)
                             + " FROM " + table + " " + extra[0], extra[1])
        except:
            raise

    def fetchone(self, table, columns, extra=("", ())):
        self._fetch(table, columns, extra)
        result = self.cur.fetchone()
        if result is None:
            return None
        if len(result) == 1:
            return result[0]
        return result

    def fetchall(self, table, columns, extra=("", ())):
        self._fetch(table, columns, extra)
        return self.cur.fetchall()

    def update(self, table, columnsdata, commit, extra, increment={}):
        try:
            first = True
            sqlstr = "UPDATE " + table + " SET "
            for col, d in columnsdata.iteritems():
                if not first:
                    sqlstr += ", "
                sqlstr += str(col) + ' = %s'
                first = False
            for col, d in increment.iteritems():
                if not first:
                    sqlstr += ", "
                sqlstr += str(col) + ' = ' + str(col) + ' + %s'
                first = False
            sqlstr += " " + extra[0]
            self.cur.execute(sqlstr,
                tuple(columnsdata.values() + increment.values()) + extra[1])
            rows = self.cur.rowcount
            if commit:
                self.db.commit()
            if rows > 0:
                return True
        except:
            self.db.rollback()
            raise
        return False

    def insert(self, table, columns_data, commit, extra=("", ())):
        column_str = self._list_to_str(columns_data.keys())
        data_str, data_param = self._list_to_sql(columns_data.values())
        try:
            self.cur.execute("INSERT INTO " + table
                             + " (" + column_str + ")"
                             + "VALUES (" + data_str + ") " + extra[0],
                             data_param + extra[1])
            rows = self.cur.rowcount
            if commit:
                self.db.commit()
            if rows == 1:
                return True
        except:
            self.db.rollback()
            raise
            return False

    def insert_purchase(self, country, card, date, discount, cart, edited,
                        location=None, status=0, syncId=None,
                        updateStock=False, note=None):
        success = False
        if dbdetails.server:
            status = 3
        if location is None:
            location = self.location
        # a unique id to identify entries: unixtimestamp + 4 random digits
        if syncId is None:
            syncId = str(util.uniqueId())
        if len(cart) == 0:
            success = True
        for boxId, quantity in cart.iteritems():
            price, containerId = self.fetchone(
                "boxes", ["price", "container"],
                (" WHERE boxesEntryId = %s", (boxId,)))
            if price is None:
                print "This boxId does not exist"
            # if discount == 10 then multiply by .9
            price = int(price * ((100 - discount) / 100.0))
            # status: 0: new, 1: edited, 2: deleted, 3: synced
            success = self.insert("cart",
                                  {"syncId": syncId, "boxId": boxId,
                                   "quantity": quantity, "price": price},
                                  False)
            # update stock
            if updateStock:
                success = success and self.update(
                        "stock",
                        {"edited": edited, "status": 1},
                        False,
                        ("WHERE location = %s AND containerId = %s",
                         (location, containerId)),
                        increment={"quantity": -quantity}
                )
        success = success and self.insert("purchases",
            {"country": country, "card": int(card),
             "date": util.datestring(date), "discount": discount,
             "status": status, "syncId": syncId, "edited": edited,
             "location": location, "note": note},
            False
        )
        if success:
            self.db.commit()
        else:
            self.db.rollback()
        return success

    def insert_shift(self, workerId, start, end, edited,
                     location=None, status=0, syncId=None):
        success = False
        if dbdetails.server:
            status = 3
        if location is None:
            location = self.location
        # a unique id to identify entries: unixtimestamp + 4 random digits
        if syncId is None:
            syncId = str(util.uniqueId())
        if end is not None:
            end = util.datestring(end)
        success = self.insert("shifts",
                {"workerId": workerId, "start": util.datestring(start),
                 "end": end, "location": location, "status": status,
                 "syncId": syncId, "edited": edited},
                False
        )
        if success:
            self.db.commit()
        else:
            self.db.rollback()
        return success

    def get_purchases(self, getDeleted=False, prettydict=False, onlydate=None,
            newerthan=None, datestring=False, notsynced=False, simplecart=False,
            allLocations=False):
        pt = "purchases"
        ct = "cart"
        bt = "boxes"
        where = ["WHERE purchases.syncId = cart.syncId "
                 + "AND boxes.boxesEntryId = cart.boxId",
                []]
        if allLocations:
            where[0] += " AND purchases.location = %s"
            where[1].append(self.location)
        if onlydate is not None:
            where[0] += " AND  purchases.date BETWEEN %s  AND %s"
            where[1].append(jinja_filters.dateformat(onlydate) + " 00:00:00")
            where[1].append(jinja_filters.dateformat(onlydate) + " 23:59:59")
        if newerthan is not None:
            where[0] += " AND  purchases.edited < %s"
            where[1].append(util.datestring(onlydate))
        if notsynced:
            where[0] += " AND  purchases.status <> 3"
        if not getDeleted:
            where[0] += " AND  purchases.status <> 2"
        result = self.fetchall(
            pt+", "+ct+", "+bt,
            [pt+".syncId", pt+".country", pt+".card", pt+".discount",
             pt+".date", pt+".status", pt+".edited", pt+".location",
             pt+".note",
             ct+".quantity", ct+".price",
             bt+".boxesEntryId", bt+".title"],
            (where[0] + " ORDER BY " + pt + ".date DESC", tuple(where[1])))
        purchases = OrderedDict()
        for row in result:
            (syncId, country, card, discount, date, status, edited,
             location, note, quantity, price, boxId, title) = row
            if datestring:
                date = util.datestring(date)
                edited = util.datestring(edited)
            key = int(syncId)
            if key not in purchases:
                purchases[key] = {}
                if prettydict:
                    purchases[key]['purchase'] = {
                        "syncId": key, "status": status, "country": country,
                        "card": card, "discount": discount, "date": date,
                        "edited": edited, "location": location, "note": note
                    }
                else:
                    purchases[key]['purchase'] = (
                            key, status, country, card, discount, date
                    )
                if simplecart:
                    purchases[key]['cart'] = {}
                else:
                    purchases[key]['cart'] = []
            if simplecart:
                purchases[key]['cart'][boxId] = quantity
            elif prettydict:
                purchases[key]['cart'].append({
                    "title": title, "boxId": boxId,
                    "quantity": quantity, "price": price
                })
            else:
                purchases[key]['cart'].append((title, boxId, quantity, price))
        return [val for k, val in purchases.iteritems()]

    def mark_purchase_deleted(self, syncId, updateStock=False):
        syncStr = str(syncId)
        edited = util.datestring(datetime.now())
        success = self.update("purchases",
            {"status": 2, "edited": edited},
            False, ("WHERE syncId = %s", (syncStr,)))
        if updateStock:
            success = success and self.cur.execute(
                "UPDATE stock, boxes, cart SET stock.edited = '" + edited + "', stock.status = 1, stock.quantity = stock.quantity + cart.quantity"
                + " WHERE stock.location = " + str(self.location) + " AND stock.containerId = boxes.container AND boxes.boxesEntryId = cart.boxId AND cart.syncId = " + syncId
            )
        if success:
            self.db.commit()
        return success

    def mark_shift_deleted(self, syncId):
        syncStr = str(syncId)
        success = self.update("shifts",
            {"status": 2, "edited": util.datestring(datetime.now())},
            False, ("WHERE syncId = %s", (syncStr,)))
        if success:
            self.db.commit()
        return success

    def delete_purchase(self, syncId):
        syncStr = str(syncId)
        try:
            self.cur.execute("DELETE FROM purchases WHERE syncId = " + syncStr)
            p_rows = self.cur.rowcount
            self.cur.execute("DELETE FROM cart WHERE syncId = " + syncStr)
            c_rows = self.cur.rowcount
            self.db.commit()
            if p_rows > 0 and c_rows > 0:
                return True
        except:
            self.db.rollback()
            raise
        return False

    def delete_shift(self, syncId):
        syncStr = str(syncId)
        try:
            self.cur.execute("DELETE FROM shifts WHERE syncId = " + syncStr)
            rows = self.cur.rowcount
            self.db.commit()
            if rows > 0:
                return True
        except:
            self.db.rollback()
            raise
        return False

    def change_purchase_status(self, syncId, status):
        return self.update("purchases", {"status": status},
                           True, ("WHERE syncId = %s", (syncId,)))

    def mark_purchase_synced(self, syncId):
        return self.change_purchase_status(syncId, 3)

    def change_shift_status(self, syncId, status):
        return self.update("shifts", {"status": status},
                           True, ("WHERE syncId = %s", (syncId,)))

    def mark_shift_synced(self, syncId):
        return self.change_shift_status(syncId, 3)

    def change_container_status(self, syncId, status):
        return self.update("stock", {"status": status},
                           True, ("WHERE syncId = %s", (syncId,)))

    def mark_container_synced(self, syncId):
        return self.change_container_status(syncId, 3)

    def get_boxes(self):
        boxes = OrderedDict()
        results = self.fetchall("boxes", ["boxesEntryId", "title", "price"])
        for result in results:
            (boxId, title, price) = result
            boxes[boxId] = {"title": title, "price": price}
        return boxes

    def update_last_sync(self, date=datetime.now()):
        self.update("config", {"last_sync": util.datestring(date)}, True, ("", ()))

    def get_last_sync(self):
        return self.fetchone("config", ["last_sync"])

    def get_version(self):
        return self.fetchone("config", ["version"])

    def begin_work(self, workerId):
        res = self.fetchone("shifts", ["workerId"],
                            ("WHERE workerId = %s AND end IS NULL",
                             (workerId,)))
        if res is not None:
            return True
        now = datetime.now()
        return self.insert_shift(workerId, now, None, now)

    def end_work(self, workerId):
        try:
            self.update("shifts", {"end": util.datestring(datetime.now())},
                True, ("WHERE workerId = %s AND end IS NULL", (workerId,)))
            return True
        except:
            # TODO write error to log
            return False

    def get_workers(self):
        working = self.fetchall("shifts", ["workerId"],
                                ("WHERE end IS NULL", ()))
        working = [w[0] for w in working] if working else []
        workers = {
                wid: {"name": wname, "working": wid in working}
                for wid, wname in util.workers.iteritems()
        }
        return workers

    def get_shifts(self, getDeleted=False, notsynced=False, datestring=False,
                   newerthan=None, returndict=False, allLocations=False):
        where = ["WHERE end IS NOT NULL", []]
        if notsynced:
            where[0] += " AND status <> 3"
        if not allLocations:
            where[0] += " AND location = %s"
            where[1].append(self.location)
        result = self.fetchall("shifts",
            ["workerId", "start", "end", "syncId", "status", "edited", "location"],
            (where[0], tuple(where[1]))
        )
        shifts = []
        for row in result:
            (workerId, start, end, syncId, status, edited, location) = row
            key = int(syncId)
            if datestring:
                start = util.datestring(start)
                end = "null" if end is None else util.datestring(end)
            if not getDeleted and status == 2:
                continue
            if newerthan is not None:
                if newerthan > edited:
                    continue
            shifts.append({"syncId": key, "workerId": workerId, "start": start,
                           "end": end, "status": status, "location": location})
        if returndict:
            shifts = {shift["syncId"]: shift for shift in shifts}
        return shifts

    def get_stock(self, allLocations=False, notsynced=False, datestring=False,
                  newerthan=None, returndict=False, containerIndexed=False):
        # the syncId check if unnecessary but done to have a first WHERE
        where = ["WHERE syncId IS NOT NULL", []]
        if not allLocations:
            where[0] += " AND location = %s"
            where[1].append(self.location)
        if notsynced:
            where[0] += " AND status <> 3"
        result = self.fetchall("stock",
            ["containerId", "quantity", "location", "syncId",
             "status", "edited", "recounted"], (where[0], tuple(where[1])))
        stock = []
        for row in result:
            (containerId, quantity, location, syncId,
             status, edited, recounted) = row
            if newerthan is not None:
                if newerthan > edited:
                    continue
            if datestring:
                edited = util.datestring(edited)
                recounted = util.datestring(recounted)
            stock.append({
                "containerId": containerId, "quantity": quantity,
                "location": location, "syncId": syncId, "status": status,
                "edited": edited, "recounted": recounted
            })
        if returndict:
            if containerIndexed:
                stock = {x["containerId"]: x for x in stock}\
                        if returndict else stock
            else:
                stock = {x["syncId"]: x for x in stock}\
                        if returndict else stock
        return stock

    def update_stock(self, containers, absolute):
        success = True
        now = util.datestring(datetime.now())
        for containerId, quantity in containers.iteritems():
            if absolute:
                success = success and self.update("stock",
                    {"quantity": quantity, "recounted": now,
                     "edited": now, "status": 1}, False,
                    ("WHERE containerId = %s AND location = %s",
                     (containerId, (self.location,))))
            else:
                success = success and self.update("stock",
                    {"edited": now, "status": 1}, False,
                    ("WHERE containerId = %s AND location = %s",
                     (containerId, (self.location,))),
                    increment={"quantity": quantity})
        self.db.commit()
        return True

    def update_container(self, syncId, containerId, quantity,
                         location, edited, recounted):
        last_recount = self.fetchone("stock", ["recounted"],
                                     ("WHERE syncId = %s", (syncId,)))
        if edited > last_recount:
            return self.update("stock",
                {"quantity": quantity, "recounted": recounted,
                 "status": 3, "edited": edited}, True,
                ("WHERE syncId = %s AND location = %s",
                 (syncId, self.location)))
