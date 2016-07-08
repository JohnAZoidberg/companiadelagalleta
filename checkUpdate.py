#!/usr/bin/python -u
# coding=utf-8
import cgitb
cgitb.enable()

import subprocess
import util

subprocess.call("./update.sh")
print "Location: update.py"
print 
