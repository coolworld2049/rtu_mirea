#!/usr/bin/env bash

set +e

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

hdfs_path=warehouse/pig/output
local_path=pig/output

hdfs dfs -rm -r $hdfs_path
pig -f pig/queries.pig

[ -d $local_path ] || mkdir -p $local_path

for i in {1..6}; do
  remote=$hdfs_path/q$i/part-*
  loc=$local_path/"$i".csv
  [ ! -f $loc ] || rm $loc
  echo "$remote" to $loc
  hdfs dfs -copyToLocal "$remote" $loc
done;
