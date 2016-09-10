#!/usr/bin/python -u
# coding=utf-8
#import logging
import sys
import os
from werkzeug.debug import DebuggedApplication
#logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from companiadelagalleta import app
app.debug = True
application = DebuggedApplication(app, True)
