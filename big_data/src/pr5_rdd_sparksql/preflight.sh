#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

HDFS_DIR=tweets

hdfs dfs -mkdir $HDFS_DIR

for file in ~/tweets/*.csv; do
  echo copy "$file" to $HDFS_DIR/"$file"
  hdfs dfs -copyFromLocal  "$file" $HDFS_DIR
done;