#!/usr/bin/python -u
# coding=utf-8
import cgitb
cgitb.enable()

import subprocess
import util

def redirect():
    print "Location: update.py"
    print 

def update():
    return subprocess.check_output("./update.sh")

if __name__ == "__main__":
    update()
    redirect()
