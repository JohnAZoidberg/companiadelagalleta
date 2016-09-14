#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from collections import OrderedDict
from datetime import datetime, timedelta
from model import *

import MySQLdb

import util
from dbdetails import dbdetails
import jinja_filters


class CgBase:
    def __init__(self, location):
        pass
        self.db = self._connectDb()
        self.db.autocommit(False)
        self.cur = self.db.cursor()
        self.dict_cur = self.db.cursor(MySQLdb.cursors.DictCursor)
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

    def _fetch(self, table, columns, extra=("", ()), returndict=False):
        try:
            sql = ("SELECT " + self._list_to_str(columns)
                             + " FROM " + table + " " + extra[0])
            if returndict:
                self.dict_cur.execute(sql, extra[1])
            else:
                self.cur.execute(sql, extra[1])
        except:
            raise

    def _fetchone(self, table, columns, extra=("", ())):
        self._fetch(table, columns, extra)
        result = self.cur.fetchone()
        if result is None:
            return None
        if len(result) == 1:
            return result[0]
        return result

    def _fetchall(self, table, columns, extra=("", ()), returndict=False):
        self._fetch(table, columns, extra, returndict=returndict)
        return self.cur.fetchall()

    def _simple_fetchall(self, sql, extras):
        self.cur.execute(sql, extras)
        return self.cur.fetchall()

    def _update(self, table, columnsdata, commit, extra, increment={}):
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

    def _insert(self, table, columns_data, commit, extra=("", ())):
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
                        location=None, status=0, syncId=None, note=None):
        if note == "":
            note = None
        if location is None:
            location = self.location
        if len(cart) == 0:
            raise Exception("Empty cart")

        cart_items = []
        for box_id, quantity in cart.iteritems():
            box = Box.query.get(box_id)
            if box is None:
                raise Exception("Box does not exists")
            price = box.price
            container_id = box.container_id

            # apply discount
            # if discount == 10 then multiply by .9
            price = int(price * ((100 - discount) / 100.0))
            price = util.round_cent(price)

            cart_items.append(CartItem(None, boxId, container_id, price))

        purchase = Purchase(location, country, card, discount,
                                  discount, cart_items)
        g.db.session.add(purchase)
        g.db.session.commit()
        success = True
        return success

    def insert_shift(self, workerId, start, end, edited,
                     location=None, status=0, syncId=None):
        success = False
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

    def update_shift(self, workerId, start, end, edited,
                     location, status, syncId):
        success = False
        # a unique id to identify entries: unixtimestamp + 4 random digits
        if syncId is None:
            syncId = str(util.uniqueId())
        if end is not None:
            end = util.datestring(end)
        success = self.update("shifts",
                {"workerId": workerId, "start": util.datestring(start),
                 "end": end, "location": location, "status": status,
                 "edited": edited},
                False,
                ("WHERE syncId = %s", (syncId,))
        )
        if success:
            self.db.commit()
        else:
            self.db.rollback()
        return success

    def update_purchase(self, country, card, date, discount, cart, edited,
                        location=None, status=1, syncId=None, note=None):
        if syncId is None:
            raise Exception("SyncId can not be None")
        delete = self.delete_purchase(syncId, edited=edited)
        insert = self.insert_purchase(country, card, date, discount, cart,
                        edited, location, status, syncId, note)
        return delete and insert

    def get_purchases(self, getDeleted=False, onlydate=None, newerthan=None,
            datestring=False, notsynced=False, simplecart=False,
            allLocations=False, notnow=False):
        where = ["WHERE purchases.syncId = cart.syncId "
                 + "AND boxes.boxesEntryId = cart.boxId",
                []]
        pt = "purchases"
        ct = "cart"
        bt = "boxes"
        if not allLocations:
            where[0] += " AND purchases.location = %s"
            where[1].append(self.location)
        if notnow:
            where[0] += " AND purchases.edited <> %s"
            where[1].append(notnow)
        if onlydate is not None:
            where[0] += " AND purchases.date BETWEEN %s  AND %s"
            where[1].append(jinja_filters.dateformat(onlydate) + " 00:00:00")
            where[1].append(jinja_filters.dateformat(onlydate) + " 23:59:59")
        if newerthan is not None:
            where[0] += " AND purchases.edited > %s"
            where[1].append(util.datestring(newerthan))
        if notsynced:
            where[0] += " AND purchases.status <> 3"
        if not getDeleted:
            where[0] += " AND purchases.status <> 2"
        result = self._fetchall(
            pt+", "+ct+", "+bt,
            [pt+".syncId", pt+".country", pt+".card", pt+".discount",
             pt+".date", pt+".status", pt+".edited", pt+".location",
             pt+".note",
             ct+".quantity", ct+".price",
             bt+".boxesEntryId", bt+".title"],
            (where[0] + " ORDER BY "+pt+".date DESC", tuple(where[1])))
        purchases = OrderedDict()
        for row in result:
            (syncId, country, card, discount, date, status, edited,
             location, note, quantity, price, boxId, title) = row
            if datestring:
                date = util.datestring(date)
                edited = util.datestring(edited)
            key = int(syncId)
            if key not in purchases:
                purchases[key] = {
                    "syncId": key, "status": status, "country": country,
                    "card": card, "discount": discount, "date": date,
                    "edited": edited, "location": location, "note": note
                }
                if simplecart:
                    purchases[key]['cart'] = {}
                else:
                    purchases[key]['cart'] = []
            if simplecart:
                purchases[key]['cart'][boxId] = quantity
            else:
                purchases[key]['cart'].append({
                    "title": title, "boxId": boxId,
                    "quantity": quantity, "price": price
                })
        return [val for k, val in purchases.iteritems()]

    def mark_purchase_deleted(self, syncId):
        syncStr = str(syncId)
        edited = util.datestring(datetime.now())
        success = self.update("purchases",
            {"status": 2, "edited": edited},
            False, ("WHERE syncId = %s", (syncStr,)))
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

    def mark_stock_item_deleted(self, syncId):
        syncStr = str(syncId)
        success = self.update("stock",
            {"status": 2, "edited": util.datestring(datetime.now())},
            False, ("WHERE syncId = %s", (syncStr,)))
        if success:
            self.db.commit()
        return success

    def delete_purchase(self, syncId, commit=True, edited=None):
        syncStr = str(syncId)
        try:
            self.cur.execute("DELETE FROM purchases WHERE syncId = " + syncStr)
            p_rows = self.cur.rowcount
            self.cur.execute("DELETE FROM cart WHERE syncId = " + syncStr)
            c_rows = self.cur.rowcount
            success = True
            if p_rows > 0 and c_rows > 0 and success:
                if commit:
                    self.db.commit()
                return True

        except:
            raise
        self.db.rollback()
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

    def delete_stock_item(self, syncId):
        syncStr = str(syncId)
        try:
            self.cur.execute("DELETE FROM stock WHERE syncId = " + syncStr)
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

    def mark_stock_item_synced(self, syncId):
        return self.update("stock", {"status": 3},
                           True, ("WHERE syncId = %s", (syncId,)))

    def get_boxes(self):
        boxes = OrderedDict()
        results = self._fetchall("boxes", ["boxesEntryId", "title", "price"])
        for result in results:
            (boxId, title, price) = result
            boxes[boxId] = {"title": title, "price": price}
        return boxes

    def update_last_sync(self, date=datetime.now()):
        self.update("config", {"last_sync": util.datestring(date)}, True, ("", ()))

    def get_last_sync(self):
        return self._fetchone("config", ["last_sync"])

    def get_version(self):
        return self._fetchone("config", ["version"])

    def begin_work(self, workerId):
        res = self._fetchone("shifts", ["workerId"],
                            ("WHERE workerId = %s AND end IS NULL",
                             (workerId,)))
        if res is not None:
            return True
        now = datetime.now()
        return self.insert_shift(workerId, now, None, now)

    def end_work(self, workerId):
        end = util.datestring(datetime.now())
        i = self.update("shifts", {"end": end, "edited": datetime.now()},
            True, ("WHERE workerId = %s AND end IS NULL", (workerId,)))
        if i == 0:
            return False
        else:
            return end

    def get_workers(self):
        working = self._fetchall("shifts", ["workerId"],
                                ("WHERE end IS NULL", ()))
        working = [w[0] for w in working] if working else []
        workers = {
                wid: {"name": wname, "working": wid in working}
                for wid, wname in util.workers.iteritems()
        }
        return workers

    def get_shifts(self, getDeleted=False, notsynced=False, datestring=False,
                   newerthan=None, returndict=False, allLocations=False,
                   notnow=False):
        where = ["WHERE end IS NOT NULL", []]
        if not allLocations:
            where[0] += " AND location = %s"
            where[1].append(self.location)
        if notnow:
            where[0] += " AND edited <> %s"
            where[1].append(notnow)
        if newerthan is not None:
            where[0] += " AND edited > %s"
            where[1].append(util.datestring(newerthan))
        if notsynced:
            where[0] += " AND status <> 3"
        if not getDeleted:
            where[0] += " AND status <> 2"
        where[0] += " ORDER BY start DESC"
        result = self._fetchall("shifts",
            ["workerId", "start", "end", "syncId", "status", "edited", "location"],
            (where[0], tuple(where[1]))
        )
        shifts = []
        for row in result:
            (workerId, start, end, syncId, status, edited, location) = row
            key = int(syncId)
            if datestring:
                start = util.datestring(start)
                edited = util.datestring(edited)
                end = "null" if end is None else util.datestring(end)
            shifts.append({"syncId": key, "workerId": workerId, "start": start,
                           "end": end, "status": status, "edited": edited,
                           "location": location})
        if returndict:
            shifts = {shift["syncId"]: shift for shift in shifts}
        return shifts

    def get_shift_stats(self, month, year):
        self.cur.execute((
            "SELECT workerId, DATE(start), start, status,"
            "       nn.end, TIMEDIFF(nn.end, start),"
            " ("
            "   SELECT COALESCE(SUM(c.price * c.quantity),0) AS total"
            "   FROM cart c, purchases p"
            "   WHERE p.location = %s AND p.status <> 2"
            "   AND c.syncId = p.syncId"
            "   AND start < p.date AND p.date < nn.end"
            " ) AS sales"
            " FROM shifts"
            " LEFT JOIN("
            "   SELECT syncId, COALESCE(end, NOW()) AS end"
            "   FROM shifts"
            " ) AS nn"
            " ON nn.syncId = shifts.syncId"
            " WHERE location = %s AND status <> 2"
            " AND MONTH(start) = %s AND YEAR(start) = %s"
            " ORDER BY start DESC"
        ), (self.location, self.location, month, year))
        result = self.cur._fetchall()
        workdays = OrderedDict()
        summary = OrderedDict()
        for row in result:
            (workerId, workdate, start, status, end, duration, sales) = row
            sales = int(sales)
            shift = {
                "workerId": workerId,
                "worker": util.all_workers[workerId],
                "duration": duration,
                "start": start,
                "end": end,
                "status": status,
                "sales": sales
            }
            try:
                summary[workerId]["hours"] += duration
                summary[workerId]["sales"] += sales
            except KeyError:
                summary[workerId] = {
                    "worker": util.all_workers[workerId],
                    "workerId": workerId,
                    "hours": duration,
                    "sales": sales
                }
            try:
                workdays[workdate].append(shift)
            except KeyError:
                workdays[workdate] = [shift]
        return workdays, summary.values()

    def get_stock(self):
        quantity_sql =(
            "SELECT i.containerId, SUM(i.quantity) AS quantity "
            "FROM ("
            "  SELECT containerId, quantity, status, location, date FROM stock "
            "  UNION ALL "
            "  SELECT boxes.container, cart.quantity * -1, purchases.status, purchases.location, purchases.date "
            "  FROM boxes, cart, purchases "
            "  WHERE purchases.syncId = cart.syncId AND cart.boxId = boxes.boxesEntryId "
            ") AS i "
            "WHERE status <> 2 AND location = %s "
            "AND date >= ("
            "  SELECT date FROM stock j "
            "  WHERE i.containerId = j.containerId "
            "  AND i.location = j.location AND recounted = 1 "
            "  ORDER BY j.date DESC LIMIT 1) "
            "GROUP BY i.containerId")
        status_sql = (
            "SELECT s1.containerId, s1.status"
            " FROM stock s1"
            " LEFT JOIN stock s2 ON s1.containerId = s2.containerId"
            "   AND s1.date < s2.date"
            " WHERE s2.containerId IS NULL"
            " AND s1.status <> 2 AND s1.location = %s"
            #" AND syncId = ("
            #"   SELECT "
            #" )"
        )
        sql = (
            "SELECT Sub1.containerId, Sub1.quantity, Sub2.status "
            "FROM (" + quantity_sql + ") Sub1 "
            "INNER JOIN (" + status_sql + ") Sub2 "
            "ON Sub1.containerId = Sub2.containerId"
        )

        result = self._simple_fetchall(sql, (self.location, self.location))
        containers = {}
        for row in result:
            (containerId, quantity, status) = row
            containers[containerId] = {
                'quantity': quantity,
                'status': status
            }
        return containers

    def get_container_stock(self, container_id):
        # TODO fetch correct location and not deleted stuff
        sql = (
            "   SELECT quantity, date, recounted"
            "   FROM stock"
            "   WHERE containerId = %s "
            "     AND status <> 2"
            " UNION ALL"
            "   SELECT cart.quantity * -1, purchases.date, 2"
            "   FROM boxes, cart, purchases "
            "   WHERE purchases.syncId = cart.syncId"
            "     AND cart.boxId = boxes.boxesEntryId"
            "     AND boxes.container = %s"
            "     AND purchases.status <> 2"
            " ORDER BY date ASC"
        )

        stats = []
        result = self._simple_fetchall(sql, (container_id, container_id))
        tally = 0
        for row in result:
            (quantity, date, recounted) = row
            if recounted == 0 or recounted == 2:
                tally += quantity
            elif recounted == 1:
                tally = quantity
            stats.append({
                "quantity": quantity,
                "date": date,
                "recounted": recounted,
                "tally": tally
            })
        return list(reversed(stats))[:50]

    def get_stock_items(self, allLocations=False, notsynced=False, datestring=False,
                  newerthan=None, returndict=False, containerIndexed=False, notnow=False):
        # the syncId check is unnecessary but done to have a first WHERE
        where = ["WHERE syncId IS NOT NULL", []]
        if not allLocations:
            where[0] += " AND location = %s"
            where[1].append(self.location)
        if newerthan is not None:
            where[0] += " AND edited > %s"
            where[1].append(util.datestring(newerthan))
        if notsynced:
            where[0] += " AND status <> 3"
        if notnow:
            where[0] += " AND edited <> %s"
            where[1].append(notnow)
        result = self.fetchall("stock",
            ["containerId", "quantity", "location", "syncId",
             "status", "edited", "recounted", "date"], (where[0], tuple(where[1])))
        stock = []
        for row in result:
            (containerId, quantity, location, syncId,
             status, edited, recounted, date) = row
            if datestring:
                edited = util.datestring(edited)
                date = util.datestring(date)
            stock.append({
                "containerId": containerId, "quantity": quantity,
                "location": location, "syncId": syncId, "status": status,
                "edited": edited, "recounted": recounted, "date": date
            })
        if returndict:
            if containerIndexed:
                stock = {x["containerId"]: x for x in stock}\
                        if returndict else stock
            else:
                stock = {x["syncId"]: x for x in stock}\
                        if returndict else stock
        return stock

    def insert_stock_item(self, containerId, quantity, recounted, edited, date,
                          location=None, status=0, syncId=None, commit=True):
        if syncId is None:
            syncId = util.uniqueId()
        if location is None:
            location = self.location
        return self.insert("stock",
                   {"containerId": containerId,
                    "quantity": quantity,
                    "location": location,
                    "syncId": syncId,
                    "status": status,
                    "edited": edited,
                    "recounted": recounted,
                    "date": date,
                   },
                   commit
        )

    def update_stock(self, containers, absolute):
        now = datetime.now()
        success = True
        for containerId, quantity in containers.iteritems():
            success = success and \
                      self.insert_stock_item(containerId, quantity,
                          absolute, now, now, commit=False)
        if success:
            self.db.commit()
        else:
            self.db.rollback()
        return success
