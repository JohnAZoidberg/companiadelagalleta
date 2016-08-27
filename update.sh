#!/bin/bash
#git pull
if [ -z "$1" ]
  then
    echo "No path supplied"
    exit 1
fi
if [ -z "$2" ]
  then
    echo "No wsgi location supplied"
    exit 1
fi
cd $1
echo "Updating..."
sudo git pull
sudo touch $2
echo "Update finished"
