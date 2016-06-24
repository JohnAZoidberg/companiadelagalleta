#!/usr/bin/python -u
# -*- coding: UTF-8 -*-
import cgitb
cgitb.enable()
print "Content-Type: text/html;charset=utf-8"
print
import MySQLdb
from dbconn import *
db = connectDb()                     
cur = db.cursor()

def insert_boxes():
    cur.execute("TRUNCATE TABLE boxes")
    try:
        boxes = [
            ("Galletas a la carta - 10", 895),
            ("Galletas a la carta - 20", 1595),
            ("Galletas a la carta - 30", 2195),
            ("Basic bag pequena - Mix", 495),
            ("Basic bag pequena - Frutas Tropicales", 495),
            ("Basic bag pequena - Sabores de Canarias", 495),
            ("Basic bag pequena - Chocolate", 495),
            ("Basic bag pequena - Clasica", 495),
            ("Basic bag grande - Mix", 995),
            ("Basic bag grande - Frutas Tropicales", 995),
            ("Basic bag grande - Sabores de Canarias", 995),
            ("Basic bag grande - Chocolate", 995),
            ("Basic bag grande - Clasica", 995),
            ("Cube box pequena - Mix", 795),
            ("Cube box pequena - Frutas Tropicales", 795),
            ("Cube box pequena - Sabores de Canarias", 795),
            ("Cube box pequena - Chocolate", 795),
            ("Cube box pequena - Clasica", 795),
            ("Cube box grande - Mix", 1195),
            ("Cube box grande - Frutas Tropicales", 1195),
            ("Cube box grande - Sabores de Canarias", 1195),
            ("Cube box grande - Chocolate", 1195),
            ("Cube box grande - Clasica", 1195),
            ("Pyramid window box - Mix", 695),
            ("Pyramid window box - Tropicales", 695),
            ("Pyramid window box - Sabores de Canarias", 695),
            ("Pyramid window box - Chocolate", 695),
            ("Pyramid window box - Clasica", 695),
            ("Elegant box 1 verde - Mix", 995),
            ("Elegant box 1 verde - Chocolate", 995),
            ("Elegant box 1 verde - Bano de chocolate", 995),
            ("Elegant box 1 crema - Mix", 995),
            ("Elegant box 1 crema - Frutas tropicales", 995),
            ("Elegant box 1 crema - Sabores de Canarias", 995),
            ("Elegant box 2 verde - Mix", 1595),
            ("Elegant box 2 verde - Chocolate", 1595),
            ("Elegant box 2 verde - Bano de chocolate", 1595),
            ("Elegant box 2 verde - Excelencia", 1595),
            ("Elegant box 2 crema - Mix", 1595),
            ("Elegant box 2 crema - Frutas tropicales", 1595),
            ("Elegant box 2 crema - Sabores de Canarias", 1595),
            ("Elegant box 2 crema - Clasica", 1595),
            ("Elegant box 3 verde - Mix", 2195),
            ("Elegant box 3 verde - Chocolate", 2195),
            ("Elegant box 3 verde - Bano de chocolate", 2195),
            ("Elegant box 3 verde - Excelencia", 2195),
            ("Elegant box 3 crema - Mix", 2195),
            ("Elegant box 3 crema - Frutas tropicales", 2195),
            ("Elegant box 3 crema - Sabores de Canarias", 2195),
            ("Elegant box 3 crema - Clasica", 2195),
            ("Strelitzia box - Mix", 1395),
            ("Strelitzia box - Sabores de Canarias", 1395),
            ("Mango box - Mix", 1395),
            ("Mango box - Excelencia", 1395),
            ("Plumeria box - Excelencia", 1895)]
        for box, price in boxes:
            cur.execute("INSERT INTO boxes (title, price) VALUES ('" + box + "', "+str(price)+")")
        db.commit()
    except:
        db.rollback()


insert_boxes()
cur.execute("SELECT * FROM boxes")

for row in cur.fetchall():
    print row
db.close
print "Hello Wörld"
