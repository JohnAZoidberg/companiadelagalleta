#!/usr/bin/python -u
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")

import os
import unittest
from datetime import datetime

basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir + '/../')

from companiadelagalleta import util, jinja_filters
from flask import Markup



class UtilTestCase(unittest.TestCase):
    def test_is_same_day(self):
        test_dates = [
            (True, datetime(2016, 8, 12, 0, 0, 0),
             datetime(2016, 8, 12, 0, 0, 0)),
            (True, datetime(2016, 8, 12, 0, 0, 0),
             datetime(2016, 8, 12, 23, 59, 59)),
            (False, datetime(2016, 8, 12, 0, 0, 0),
             datetime(2016, 8, 11, 0, 0, 0)),
            (False, datetime(2016, 8, 12, 0, 0, 0),
             datetime(2016, 8, 11, 23, 59, 59))
        ]
        for (result, first, second) in test_dates:
            self.assertEqual(result, util.is_same_day(first, second))

    def test_earlier_than(self):
        assert not util.earlier_than(
            12, 0, datetime(2016, 8, 12, 12, 0, 0))
        assert util.earlier_than(
            12, 1, datetime(2016, 8, 12, 12, 0, 0))
        assert not util.earlier_than(
            12, 0, datetime(2016, 8, 12, 12, 0, 1))
        assert util.earlier_than(
            12, 0, datetime(2016, 8, 12, 11, 0, 0))

class JinjaFiltersTestCase(unittest.TestCase):
    def test_money_format(self):
        money_vals = {
            "10.05&nbsp;€": 100500,
            "10.50&nbsp;€": 105000,
            "10.00&nbsp;€": 100000,
            "1.00&nbsp;€": 10000,
            "0.10&nbsp;€": 1000,
            "0.01&nbsp;€": 100
        }
        for formatted, raw in money_vals.iteritems():
            self.assertEqual(Markup(formatted),
                             jinja_filters.moneyformat(raw))

    def test_readable_version(self):
        versions = {
            "1.0.0": 10000,
            "0.8.0": 800,
            "0.12.0": 1200
        }
        for formatted, raw in versions.iteritems():
            self.assertEqual(formatted,
                             jinja_filters.readable_version(raw))

if __name__ == '__main__':
    unittest.main()
