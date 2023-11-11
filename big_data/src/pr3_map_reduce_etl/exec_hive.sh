#!/usr/bin/env bash

args=("$@")
sudo docker exec -it hiveserver2-standalone beeline -u jdbc:hive2://hiveserver2-standalone:10000/ -n "$(whoami)" --color=true "${args[@]}"
