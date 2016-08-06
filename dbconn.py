#!/usr/bin/python -u
# coding=utf-8
import util
from collections import OrderedDict
from datetime import datetime

import MySQLdb

from dbdetails import dbdetails


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

    def _list_to_str(self, xs, quote=""):  # TODO rename to _list_to_sql_str
        str_value = quote + str(xs[0]) + quote
        for x in xs[1:]:
            if x is None:
                str_value += ", NULL"
            else:
                str_value += ", " + quote + str(x) + quote
        return str_value

    def _fetch(self, table, columns, extra=""):
        try:
            self.cur.execute("SELECT " + self._list_to_str(columns)
                             + " FROM " + table + " " + extra)
        except:
            raise

    def fetchone(self, table, columns, extra=""):
        self._fetch(table, columns, extra)
        result = self.cur.fetchone()
        if result is None:
            return None
        if len(result) == 1:
            return result[0]
        return result

    def fetchall(self, table, columns, extra=""):
        self._fetch(table, columns, extra)
        return self.cur.fetchall()

    def update(self, table, columnsdata, commit, extra, increment={}):
        try:
            first = True
            sqlstr = "UPDATE " + table + " SET "
            for col, d in columnsdata.iteritems():
                if not first:
                    sqlstr += ", "
                try:
                    d = int(d)
                    sqlstr += str(col) + ' = ' + str(d)
                except:
                    sqlstr += str(col) + ' = "' + str(d) + '"'
                first = False
            for col, d in increment.iteritems():
                if not first:
                    sqlstr += ", "
                sqlstr += str(col) + ' = ' + str(col) + '+' + str(int(d))
                first = False
            sqlstr += " " + extra
            self.cur.execute(sqlstr)
            rows = self.cur.rowcount
            if commit:
                self.db.commit()
            if rows > 0:
                return True
        except:
            self.db.rollback()
            raise
        return False

    def insert(self, table, columns_data, commit, extra=""):
        column_str = self._list_to_str(columns_data.keys())
        data_str = self._list_to_str(columns_data.values(), '"')
        try:
            self.cur.execute("INSERT INTO " + table
                             + " (" + column_str + ")"
                             + "VALUES (" + data_str + ") " + extra)
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
                " WHERE boxesEntryId = " + str(boxId))
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
                        "WHERE location = " + str(location)
                        + " AND containerId = " + str(containerId),
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
        where = "" if allLocations else " AND location = " + str(self.location)
        pt = "purchases"
        ct = "cart"
        bt = "boxes"
        result = self.fetchall(
            pt+", "+ct+", "+bt,
            [pt+".syncId", pt+".country", pt+".card", pt+".discount",
             pt+".date", pt+".status", pt+".edited", pt+".location",
             pt+".note",
             ct+".quantity", ct+".price",
             bt+".boxesEntryId", bt+".title"],
            "WHERE purchases.syncId = cart.syncId "
            + "AND boxes.boxesEntryId = cart.boxId" + where
            + " ORDER BY " + pt + ".date DESC")
        purchases = OrderedDict()
        for row in result:
            (syncId, country, card, discount, date, status, edited,
             location, note, quantity, price, boxId, title) = row
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
            False, "WHERE syncId=" + syncStr)
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
            False, "WHERE syncId=" + syncStr)
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
                           True, "WHERE syncId=" + str(syncId))

    def mark_purchase_synced(self, syncId):
        return self.change_purchase_status(syncId, 3)

    def change_shift_status(self, syncId, status):
        return self.update("shifts", {"status": status},
                           True, "WHERE syncId=" + str(syncId))

    def mark_shift_synced(self, syncId):
        return self.change_shift_status(syncId, 3)

    def change_container_status(self, syncId, status):
        return self.update("stock", {"status": status},
                           True, "WHERE syncId=" + str(syncId))

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
        self.update("config", {"last_sync": util.datestring(date)}, True, "")

    def get_last_sync(self):
        return self.fetchone("config", ["last_sync"], "")

    def get_version(self):
        return self.fetchone("config", ["version"])

    def begin_work(self, workerId):
        res = self.fetchone("shifts", ["workerId"],
                            "WHERE workerId = " + workerId + " AND end IS NULL")
        if res is not None:
            return True
        now = datetime.now()
        return self.insert_shift(workerId, now, None, now)

    def end_work(self, workerId):
        try:
            self.update("shifts", {"end": util.datestring(datetime.now())},
                        True, "WHERE workerId = " + workerId + " AND end IS NULL")
            return True
        except:
            # TODO write error to log
            return False

    def get_workers(self):
        working = self.fetchall("shifts", ["workerId"], "WHERE end IS NULL")
        working = [w[0] for w in working] if working else []
        workers = {
                wid: {"name": wname, "working": wid in working}
                for wid, wname in util.workers.iteritems()
        }
        return workers

    def get_shifts(self, getDeleted=False, notsynced=False, datestring=False,
                   newerthan=None, returndict=False, allLocations=False):
        where = "WHERE end IS NOT NULL"
        where += " AND status <> 3" if notsynced else ""
        where += " AND location = " + str(self.location) if not allLocations else ""
        result = self.fetchall("shifts",
            ["workerId", "start", "end", "syncId", "status", "edited", "location"],
            where
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
        where = ""
        if not allLocations:
            where += "WHERE location = " + str(self.location)
        if notsynced:
            if where == "":
                where += "WHERE status <> 3"
            else:
                where += " AND status <> 3"
        result = self.fetchall("stock",
            ["containerId", "quantity", "location", "syncId",
             "status", "edited", "recounted"], where)
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
                    "WHERE containerId = " + str(containerId)
                    + " AND location = " + str(self.location))
            else:
                success = success and self.update("stock",
                    {"edited": now, "status": 1}, False,
                    "WHERE containerId = " + str(containerId)
                    + " AND location = " + str(self.location),
                    increment={"quantity": quantity})
        self.db.commit()
        return True

    def update_container(self, syncId, containerId, quantity,
                         location, edited, recounted):
        last_recount = self.fetchone("stock", ["recounted"],
                                     "WHERE syncId = " + str(syncId))
        if edited > last_recount:
            return self.update("stock",
                {"quantity": quantity, "recounted": recounted,
                 "status": 3, "edited": edited}, True,
                "WHERE syncId = " + str(syncId)
                + " AND location = " + str(location))
