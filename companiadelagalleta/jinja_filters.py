# coding=utf-8
from datetime import timedelta

from jinja2.utils import Markup

import util


def dateformat(value):
    return value.strftime('%Y-%m-%d')


def datetimeformat(value):
    return value.strftime('%Y-%m-%d %H:%M')


def timeformat(value):
    return value.strftime('%H:%M')


def moneyformat(value):
    extrazero = "0" if value % 1000 == 0 else ""
    return Markup(str((value / 10000.0)) + extrazero + "&nbsp;€")


def countryformat(value):
    return util.country_list[value]


def cardformat(value):
    return "VISA" if value else ""


def discountformat(value):
    return "(-" + str(value) + "%) " if value > 0 else ""


def adddays(date, summand):
    return date + timedelta(days=summand)


def readable_version(value):
    version_str = str(value % 100)
    for i in xrange(1):
        value = value / 100
        version_str = str(value % 100) + "." + version_str
    value = value / 100
    version_str = str(value) + "." + version_str
    return version_str


def durationformat(value):
    seconds = value.total_seconds()
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    hourzero = "0" if hours < 10 else ""
    hourzero = "-0" if hours > -10 and hours < 0 else ""
    minutezero = "0" if minutes < 10 else ""
    return '{}{}:{}{}'.format(hourzero, hours, minutezero, minutes)


def weekdayformat(value):
    return util.weekdays[value.weekday()]


def monthformat(value):
    return util.months[value]

def recountedformat(value):
    if value == 0:
        return "Addition"
    elif value == 1:
        return ""
    elif value == 2:
        return "Purchase"
