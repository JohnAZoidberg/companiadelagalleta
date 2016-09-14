#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import cgitb
cgitb.enable()  # Displays any errors

from functools import partial
from datetime import datetime
import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

import util

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

    def __init__(self, id, name, active):
        self.id = id
        self.name = name
        self.active = active

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "active": self.active
        })

    def __repr__(self):
        return '<Worker {}>'.format(self.name)


class Container(db.Model):
    __tablename__ = "containers"
    id = db.Column(db.Integer, primary_key=True)

    name = NonNullColumn(db.String(255))

    boxes = db.relationship('Box', backref='containers')
    stock = db.relationship('StockItem', backref='containers')

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "boxes": str(self.boxes),
            "stock": str(self.stock)
        })

    def __repr__(self):
        return '<Container {}>'.format(self.name)


class Box(db.Model):
    __tablename__ = "boxes"
    id = db.Column(db.Integer, primary_key=True)

    name = NonNullColumn(db.String(255))
    price = NonNullColumn(db.Integer)
    container_id = NonNullColumn(db.Integer, db.ForeignKey('containers.id'))
    cart_item = db.relationship('CartItem')

    def __init__(self, name, price, container_id):
        self.name = name
        self.price = price
        self.container_id = container_id

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "container_id": self.container_id
        })

    def __repr__(self):
        return '<Box {}>'.format(self.name)


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
    note = NonNullColumn(db.Text())
    total = 0

    cart = db.relationship('CartItem', backref='purchases', lazy="joined")

    @hybrid_property
    def total(self):
        sum = 0
        for item in self.cart:
            sum += item.total
        return sum

    def __init__(self, location, country, card, discount, date, cart,
                 sync_id=None, edited=None, status=0):
        self.location = location
        self.country = country
        self.card = card
        self.discount = discount
        self.date = date

        if sync_id is None:
            sync_id = util.uniqueId()
        if edited is None:
            edited = datetime.now()
        self.sync_id = sync_id
        self.edited = edited
        self.status = status
        for item in cart:
            item.sync_id = self.sync_id
            self.cart.append(item)

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "sync_id": self.sync_id,
            "edited": util.datestring(self.edited),
            "status": self.status,
            "location": self.location,
            "country": self.country,
            "card": self.card,
            "discount": self.discount,
            "date": util.datestring(self.date),
            "cart": str(self.cart)
        })

    def __repr__(self):
        return '<Purchase {}>'.format(self.sync_id)


class CartItem(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)

    purchase_id = NonNullColumn(db.Integer, db.ForeignKey('purchases.id'))

    box_id = NonNullColumn(db.Integer, db.ForeignKey('boxes.id'))
    box = db.relationship("Box")
    quantity = NonNullColumn(db.Integer)
    price = NonNullColumn(db.Integer)

    @hybrid_property
    def total(self):
        return self.quantity * self.price

    def __init__(self, sync_id, box_id, quantity, price):
        self.sync_id = sync_id
        self.box_id = box_id
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "purchase_id": self.purchase_id,
            "box_id": self.box_id,
            "quantity": self.quantity,
            "price": self.price
        })

    def __repr__(self):
        return '<CartItem {}, {}, {}>'.format(
            self.box_id, self.quantity, self.price)


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

    def __init__(self, location, worker_id, start, end=None,
                 sync_id=None, edited=None, status=0):
        self.location = location
        self.worker_id = worker_id
        self.start = start
        self.end = end

        if sync_id is None:
            sync_id = util.uniqueId()
        if edited is None:
            edited = datetime.now()
        self.sync_id = sync_id
        self.edited = edited

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "sync_id": self.sync_id,
            "edited": util.datestring(self.edited),
            "status": self.status,
            "location": self.location,
            "worker_id": self.worker_id,
            "start": util.datestring(self.start),
            "end": util.datestring(self.end),
        })

    def __repr__(self):
        return '<Shift {}>'.format(self.worker_id)


class StockItem(db.Model):
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

    def __init__(self, location, container_id, quantity, recounted, date,
                 sync_id=None, edited=None, status=0):
        self.location = location
        self.container_id = container_id
        self.quantity = quantity
        self.recounted = recounted
        self.date = date

        if sync_id is None:
            sync_id = util.uniqueId()
        if edited is None:
            edited = datetime.now()
        self.sync_id = sync_id
        self.edited = edited

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "sync_id": self.sync_id,
            "edited": util.datestring(self.edited),
            "status": self.status,
            "location": self.location,
            "container_id": self.container_id,
            "quantity": self.quantity,
            "recounted": self.recounted,
            "end": util.datestring(self.end),
        })

    def __repr__(self):
        return '<Stock {}>'.format(self.container_id)
