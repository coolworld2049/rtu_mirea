#!/usr/bin/env bash

set -eou pipefail

if [ -f "$1" ]; then
  QUERY=$(cat "$1")
else
  QUERY="$1"
fi

sudo docker exec -it hiveserver2-standalone beeline -u jdbc:hive2://hiveserver2-standalone:10000/ -n "$(whoami)" --color=true -e "$QUERY"
