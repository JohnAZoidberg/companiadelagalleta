#!/bin/bash
#git pull
if [ -z "$1" ]
  then
    echo "No path supplied"
    exit 1
fi
cd $1
echo "Updating..."
sudo git checkout -- .
sudo git pull
echo "Update finished"
sudo /etc/init.d/apache2 reload
echo "Apache reloaded"
