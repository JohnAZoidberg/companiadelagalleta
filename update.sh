#!/bin/bash
rm *.pyc
git add log.txt
git checkout -- .
git pull
