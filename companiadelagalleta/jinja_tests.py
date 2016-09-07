# coding=utf-8
from datetime import datetime

import util


def continent(value):
    return value[0] == "_"


def today(value):
    return util.is_same_day(datetime.now(), value)

def sameDayAs(value1, value2):
    return util.is_same_day(value1, value2)
