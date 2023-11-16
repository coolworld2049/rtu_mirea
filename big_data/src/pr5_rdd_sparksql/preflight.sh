#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

hdfs dfs -mkdir tweets

for file in ~/tweets/*.csv; do
  hdfs dfs -copyFromLocal  "$file" tweets/"$file"
done;