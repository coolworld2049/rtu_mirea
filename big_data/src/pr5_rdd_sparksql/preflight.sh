#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

HDFS_DIR=tweets
LOCAL_DIR=$HOME/tweets

hdfs dfs -mkdir $HDFS_DIR

for file in "$LOCAL_DIR"/*; do
  file_name="$(basename "$file")"
  echo copy "$file" to "$HDFS_DIR"/"$file_name"
  hdfs dfs -copyFromLocal "$file" $HDFS_DIR
done;