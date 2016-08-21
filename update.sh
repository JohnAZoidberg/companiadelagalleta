#!/bin/bash
sudo chmod 666 log.txt
sudo git checkout -- .
sudo git pull

PIP_MODULES=$(pip list)
if ! [[ $PIP_MODULES == *"Flask"* ]]
then
  sudo -H pip install Flask
fi
