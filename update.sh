#!/bin/bash
rm -f *.pyc
chmod 777 log.txt
git checkout -- .
git pull
