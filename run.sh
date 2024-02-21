#!/bin/bash
if [ $USER != root ]
then
  echo -e "Please make sure you run this as root!\nExiting!"
  exit
fi

echo -e "pulling latest docker image...\n"
docker image pull itzg/minecraft-server > /dev/null

source env/bin/activate

python3 app.py