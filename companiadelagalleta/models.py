#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from functools import partial

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# todo relations, check(status)
NonNullColumn = partial(db.Column, nullable=False)
NullableColumn = partial(db.Column, nullable=True)


class Worker(db.Model):
    __tablename__ = "workers"
    id = db.Column(db.Integer, primary_key=True)

    name = NonNullColumn(db.String(255))
    active = NonNullColumn(db.Boolean())

    shifts = db.relationship('Shift', backref='workers')


class Container(db.Model):
    __tablename__ = "containers"
    id = db.Column(db.Integer, primary_key=True)

    name = NonNullColumn(db.String(255))

    boxes = db.relationship('Box', backref='containers')
    stock = db.relationship('StockItem', backref='containers')


class Box(db.Model):
    __tablename__ = "boxes"
    id = db.Column(db.Integer, primary_key=True)

    title = NonNullColumn(db.String(255))
    price = NonNullColumn(db.Integer)
    container_id = NonNullColumn(db.Integer, db.ForeignKey('container.id'))


class CartItem(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)

    sync_id = NonNullColumn(db.Integer, db.ForeignKey('cart.sync_id'),
                            unique=True)

    box_id = NonNullColumn(db.Integer, db.ForeignKey('box.id'))
    quantity = NonNullColumn(db.Integer)
    price = NonNullColumn(db.Integer)


class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True)

    sync_id = NonNullColumn(db.Integer, unique=True)

    edited = NonNullColumn(db.DateTime())
    status = NonNullColumn(db.Integer)
    location = NonNullColumn(db.Integer)

    country = NonNullColumn(db.String(50))
    card = NonNullColumn(db.Boolean())
    discount = NonNullColumn(db.Integer)
    date = NonNullColumn(db.DateTime())

    cart = db.relationship('CartItem', backref='purchases')


class Shift(db.Model):
    __tablename__ = "shifts"
    id = db.Column(db.Integer, primary_key=True)

    sync_id = NonNullColumn(db.Integer, unique=True)
    edited = NonNullColumn(db.DateTime())
    status = NonNullColumn(db.Integer)
    location = NonNullColumn(db.Integer)

    worker_id = NonNullColumn(db.Integer, db.ForeignKey('workers.id'))
    start = NonNullColumn(db.DateTime())
    end = NullableColumn(db.DateTime())


class Stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)

    sync_id = NonNullColumn(db.Integer, unique=True)
    edited = NonNullColumn(db.DateTime())
    status = NonNullColumn(db.Integer)
    location = NonNullColumn(db.Integer)

    container_id = NonNullColumn(db.Integer, db.ForeignKey('containers.id'))
    quantity = NonNullColumn(db.Integer)
    recounted = NonNullColumn(db.Boolean)
    date = NonNullColumn(db.DateTime())
