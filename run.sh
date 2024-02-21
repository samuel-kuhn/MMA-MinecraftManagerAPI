#!/bin/bash
echo -e "pulling latest docker image...\n"
docker image pull itzg/minecraft-server > /dev/null
python3 app.py