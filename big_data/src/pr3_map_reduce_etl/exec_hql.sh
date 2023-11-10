#!/usr/bin/env bash

USER="$(whoami)"
QUERY=$(cat "$1")
sudo docker exec -it hiveserver2-standalone beeline -u jdbc:hive2://hiveserver2-standalone:10000/ -n $USER --color=true -e "$QUERY"
