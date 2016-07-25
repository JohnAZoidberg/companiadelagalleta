#!/bin/bash
rm *.pyc
chmod 777 log.txt
git checkout -- .
git pull
