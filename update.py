#!/usr/bin/python -u
# coding=utf-8
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
import subprocess

def git_update():
    return subprocess.check_output("./update.sh")

def db_update():
    base = CgBase()
    new_version = 120 # 0.1.20
    version = 0
    try:
        version = base.get_version() 
    except Exception as e:
        if str(e) == "(1146, \"Table 'cg.config' doesn't exist\")":
            version = 0 # 0.0.0
    if version < 10: # 0.1.0
        carts = base.fetchall("cart", ["syncId"], "")
        purchases = base.fetchall("purchases", ["syncId"], "") 
        for cart in carts:
            if cart not in purchases:
                print cart, (cart in purchases), util.br
                sql = "DELETE FROM cart WHERE syncId=" + str(cart[0])
                base.cur.execute(sql)
        base.cur.execute("DELETE FROM cart WHERE syncId=482836353 AND boxId=17 LIMIT 1")
        try:
            base.cur.execute("ALTER TABLE cart DROP COLUMN edited")
        except:
           pass
        try:
            base.cur.execute("ALTER TABLE cart DROP COLUMN status")
        except:
           pass
        try:
            base.cur.execute("DROP TABLE config")
        except:
            pass
        base.db.commit()
        try:
            sql = (
                  "CREATE TABLE config ("
                  "constant CHAR(1) DEFAULT 'X' NOT NULL PRIMARY KEY,"
                  "CHECK (constant = 'X'),"
                  "version int DEFAULT 10 NOT NULL,"
                  "last_sync datetime DEFAULT '2016-01-01 00:00:00' NOT NULL"
                  ")"
                  )
            base.cur.execute(sql)
            base.cur.execute("INSERT INTO config () VALUES ()")
        except:
            base.db.rollback()
            raise
        base.insert("boxes", {"title": "Basic bag pequeña - GRATIS", "price": 0, "boxesEntryId": 65}, False)
        base.db.commit()
    if version < 12:
        print "This version does not add anything new :P", util.br
    if version < 117:
        base.insert("boxes", {"title": "Bolsa Merienda", "price": 275, "boxesEntryId": 66}, True)
    if version < 118:
        box_update = {
            25: "Pyramid box - Tropicales",
            26: "Pyramid box - Sabores de Canarias",
            27: "Pyramid box - Chocolate",
            28: "Pyramid box - Clásica"
        }
        for old_title, new_title in box_update.iteritems():
            base.update("boxes", {"title": new_title}, False, "WHERE boxesEntryId = " + str(old_title))
        base.db.commit()
        print "Removed the 'window' from the names of the Pyramid boxes", util.br
    if version < 119:
        box_update = {
             5: "Basic bag pequeña - Frutas",
             6: "Basic bag pequeña - Canarias",
            10: "Basic bag grande - Frutas",
            11: "Basic bag grande - Canarias",
            15: "Cube pequeña - Frutas",
            16: "Cube pequeña - Canarias",
            17: "Cube pequeña - Chocolate",
            18: "Cube pequeña - Clásica",
            20: "Cube grande - Frutas",
            21: "Cube grande - Canarias",
            22: "Cube grande - Chocolate",
            23: "Cube grande - Clásica",
            25: "Pyramid - Frutas",
            26: "Pyramid - Canarias",
            27: "Pyramid - Chocolate",
            28: "Pyramid - Clásica"
        }
        for old_title, new_title in box_update.iteritems():
            base.update("boxes", {"title": new_title}, False, "WHERE boxesEntryId = " + str(old_title))
        base.db.commit()
        print "Shorter names for the boxes", util.br
    if version < 120:
        country_changes = {
            "??": "_??",
            "eu": "_eu",
            "asia": "_asia",
            "america": "_america",
            "xx": "_xx"
        }
        for old, new in country_changes.iteritems():
            base.update("purchases", {"country": new}, False, "WHERE country='"+old+"'")
        base.cur.execute("ALTER TABLE purchases MODIFY country VARCHAR(255)")
        base.db.commit()
        print "More countries and continents", util.br

    if new_version is not None:
        base.update("config", {"version": new_version}, True, "WHERE constant = 'X'")
    if version != new_version:
        print "Updated to version: ", new_version, util.br
    else:
        print "No update available", util.br

if __name__ == "__main__":
    util.print_header()
    db_update()
