#!/usr/bin/env bash

set +e

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

hdfs_path=warehouse/pig/output
local_path=pig/query_result

[ -d $local_path ] || mkdir -p $local_path

hdfs dfs -rm -r $hdfs_path
pig -f pig/queries.pig

for i in {1..7}; do
  remote="$hdfs_path/q$i/part*"
  loc=$local_path/"$i".csv
  echo "$remote" to $loc
  hdfs dfs -copyToLocal "$remote" $loc
done;
