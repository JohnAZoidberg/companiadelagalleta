#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

import subprocess

import jinja_filters
from dbconn import CgBase
import util


def git_update():
    process = subprocess.Popen(["./update.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    returncode = process.wait()
    return (returncode == 0, process.stdout.read())


def db_update():
    result = ""
    base = CgBase(0)#util.get_location()[1])
    new_version = 600  # 0.6.0
    version = 0
    failure = False
    try:
        version = base.get_version()
    except Exception as e:
        if str(e) == "(1146, \"Table 'cg.config' doesn't exist\")":
            version = 0  # 0.0.0
    if version < 10:  # 0.1.0
        carts = base.fetchall("cart", ["syncId"])
        purchases = base.fetchall("purchases", ["syncId"])
        for cart in carts:
            if cart not in purchases:
                result += str(cart)+str(cart in purchases)+"\n"
                sql = "DELETE FROM cart WHERE syncId=" + str(cart[0])
                base.cur.execute(sql)
        base.cur.execute(
            "DELETE FROM cart WHERE syncId=482836353 AND boxId=17 LIMIT 1")
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
            base.db.commit()
        except:
            base.db.rollback()
            raise
        base.insert("boxes",
                    {"title": "Basic bag pequeña - GRATIS", "price": 0,
                     "boxesEntryId": 65},
                    False)
        base.db.commit()
    if version < 12:
        result += "This version does not add anything new :P\n",
    if version < 117:
        base.insert("boxes",
                    {"title": "Bolsa Merienda", "price": 275,
                     "boxesEntryId": 66},
                    True)
        base.db.commit()
    if version < 118:
        box_update = {
            25: "Pyramid box - Tropicales",
            26: "Pyramid box - Sabores de Canarias",
            27: "Pyramid box - Chocolate",
            28: "Pyramid box - Clásica"
        }
        for old_title, new_title in box_update.iteritems():
            base.update("boxes",
                        {"title": new_title}, False,
                        ("WHERE boxesEntryId = %s", old_title))
        result += "Removed the 'window' from the names of the Pyramid boxes\n"
        base.db.commit()
    if version < 119:
        box_update = {
            5:  "Basic bag pequeña - Frutas",
            6:  "Basic bag pequeña - Canarias",
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
            base.update("boxes", {"title": new_title}, False,
                        ("WHERE boxesEntryId = %s", old_title))
        result += "Shorter names for the boxes\n"
        base.db.commit()
    if version < 120:
        country_changes = {
            "??": "_??",
            "eu": "_eu",
            "asia": "_asia",
            "america": "_america",
            "xx": "_xx"
        }
        for old, new in country_changes.iteritems():
            base.update("purchases", {"country": new}, False,
                        ("WHERE country= %s", old))
        base.cur.execute("ALTER TABLE purchases MODIFY country VARCHAR(255)")
        result += "More countries and continents\n"
        base.db.commit()
    if version < 121:
        result += "Just an logging update for the server - don't worry\n"
    if version < 130:
        sql = (
              "CREATE TABLE shifts ("
              "workerId int NOT NULL,"
              "start datetime,"
              "end datetime,"
              "syncId int(11) NOT NULL PRIMARY KEY,"
              "status int NOT NULL,"
              "edited datetime DEFAULT '2016-01-01 00:00:00' NOT NULL,"
              "location int NOT NULL"
              ")"
        )
        base.cur.execute(sql)
        result += "New tracking for work hours\n"
    if version < 131:
        box_update = {
            15: "Cube pequeño - Frutas",
            16: "Cube pequeño - Canarias",
            17: "Cube pequeño - Chocolate",
            18: "Cube pequeño - Clásica",
            30: "Elegant 1 verde - Chocolate",
            31: "Elegant 1 verde - Baño",
            33: "Elegant 1 crema - Frutas",
            34: "Elegant 1 crema - Canarias",
            36: "Elegant 2 verde - Chocolate",
            37: "Elegant 2 verde - Baño",
            38: "Elegant 2 verde - Excelencia",
            40: "Elegant 2 crema - Frutas",
            42: "Elegant 2 crema - Clásica",
            41: "Elegant 2 crema - Canarias",
            44: "Elegant 3 verde - Chocolate",
            45: "Elegant 3 verde - Baño",
            46: "Elegant 3 verde - Excelencia",
            48: "Elegant 3 crema - Frutas",
            49: "Elegant 3 crema - Canarias",
            50: "Elegant 3 crema - Clásica",
            52: "Strelitzia - Canarias",
            54: "Mango - Excelencia",
            55: "Plumeria - Excelencia",
            58: "Cube pequeño - Vegano",
            59: "Cube grande - Vegano",
            60: "Elegant 1 verde - Vegano",
            61: "Elegant 1 crema - Vegano",
            62: "Strelitzia - Vegano",
            64: "Mango - Vegano",
        }
        for old_title, new_title in box_update.iteritems():
            base.update("boxes", {"title": new_title}, False,
                        "WHERE boxesEntryId = " + str(old_title))
        result += "Shorter names for the boxes\n"
        base.db.commit()
    if version < 400:
        try:
            base.cur.execute("ALTER TABLE purchases ADD location INT")
            base.cur.execute("UPDATE purchases SET location = 0")
            base.cur.execute(
                "ALTER TABLE purchases MODIFY COLUMN location INT NOT NULL")
            base.db.commit()
            result += "New feature for choosing location.\n"
        except:
            base.db.rollback()
            failure = True
        result += "New versioning\n"

    if version < 500:
        # Add container id o boxes table
        try:
            base.cur.execute("ALTER TABLE boxes ADD container INT")
        except:
           pass
        for container, details in util.containers.iteritems():
            for box in details['boxes']:
                sql = ("UPDATE boxes SET container = " + str(container)
                      + " WHERE `boxesEntryId` = " + str(box))
                base.cur.execute(sql)
        base.cur.execute(
            "ALTER TABLE boxes MODIFY COLUMN container INT NOT NULL")

        # Add stock table
        sql = (
              "CREATE TABLE stock ("
              "containerId INT NOT NULL,"
              "quantity INT DEFAULT 0 NOT NULL,"
              "location INT NOT NULL,"
              "syncId int(11) NOT NULL PRIMARY KEY,"
              "status int DEFAULT 3 NOT NULL,"
              "edited datetime DEFAULT '2016-01-01 00:00:00' NOT NULL,"
              "recounted datetime DEFAULT '2016-01-01 00:00:00' NOT NULL"
              ")"
              )
        base.cur.execute(sql)
        for locationId in util.locations.keys():
            for container in util.containers.keys():
                base.insert("stock",
                            {"containerId": container, "location": locationId,
                             "syncId": (container*1000+locationId)},
                            False)

        base.db.commit()
        result += "Add stock tracking\n"
    if version < 501:
        try:
            base.cur.execute("ALTER TABLE purchases ADD note TEXT")
        except:
            pass
        result += "Add feature to add notes to a purchase\n"
    if version < 502:
        try:
            price_change = {
                # Basic bags 495 => 545
                5: 545,
                6: 545,
                7: 545,
                8: 545,
                # Strelitzia 1395 => 1495
                52: 1495,
                # Mango 1395 => 1495
                54: 1495,
                # Plumeria 1895 => 1995
                55: 1995
            }
            for boxId, newPrice in price_change.iteritems():
                base.update("boxes", {"price": newPrice}, False,
                            ("WHERE boxesEntryId = %s", (boxId,)))
            base.db.commit()
            result += "Change prices of mango, basic peq, plumeria and strelitzia\n"
        except Exception as e:
            result += str(e) + "\n"
            failure = True
            base.db.rollback()
            raise
    if version < 600:
        result += "Hopefully much faster now \n"
        base.cur.execute("TRUNCATE TABLE stock")
        base.cur.execute(
            "ALTER TABLE stock MODIFY recounted BOOLEAN NOT NULL")
        base.cur.execute(
            "ALTER TABLE stock MODIFY status INT NOT NULL DEFAULT 0")
        base.db.commit()
        result += "Change how stock is counted \n"
        result += "Enable possibility of stock history \n"
    if True:
        for locationId in util.locations.keys():
            for container in util.containers.keys():
                base.insert("stock",
                            {"containerId": container, "location": locationId,
                             "syncId": (container*1000+locationId),
                             "quantity": 0, "recounted": True},
                            False)

        base.db.commit()

    if new_version is not None and not failure:
        base.update("config",
                    {"version": new_version}, True, ("WHERE constant = 'X'", ()))
        base.db.commit()
    else:
        base.db.rollback()
    if version != new_version:
        if not failure:
            result += ("Updated from " + jinja_filters.readable_version(version)
                       + " to " + jinja_filters.readable_version(new_version)+"\n")
        else:
            result += "FAILURE!\n"
    else:
        result += "No update available("+jinja_filters.readable_version(version)+")\n"
    return result

if __name__ == "__main__":
    util.print_header()
    print db_update()
