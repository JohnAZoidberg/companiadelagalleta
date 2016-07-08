#!/usr/bin/python -u
# coding=utf-8
import cgitb
cgitb.enable()

import subprocess
import util

def redirect():
    print "Location: update.py"
    print 

output = subprocess.check_output("./update.sh")
redirect()
