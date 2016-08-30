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

from companiadelagalleta import util



class FlaskrTestCase(unittest.TestCase):
    def test_is_same_day(self):
        assert util.is_same_day(datetime(2016, 8, 12, 0, 0, 0),
                                datetime(2016, 8, 12, 0, 0, 0))
        assert util.is_same_day(datetime(2016, 8, 12, 0, 0, 0),
                                datetime(2016, 8, 12, 23, 59, 59))
        assert not util.is_same_day(datetime(2016, 8, 12, 0, 0, 0),
                                    datetime(2016, 8, 11, 0, 0, 0))
        assert not util.is_same_day(datetime(2016, 8, 12, 0, 0, 0),
                                    datetime(2016, 8, 11, 23, 59, 59))

    def test_earlier_than(self):
        assert not util.earlier_than(
            12, 0, datetime(2016, 8, 12, 12, 0, 0))
        assert util.earlier_than(
            12, 1, datetime(2016, 8, 12, 12, 0, 0))
        assert not util.earlier_than(
            12, 0, datetime(2016, 8, 12, 12, 0, 1))
        assert util.earlier_than(
            12, 0, datetime(2016, 8, 12, 11, 0, 0))

if __name__ == '__main__':
    unittest.main()
