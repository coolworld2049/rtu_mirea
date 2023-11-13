#!/bin/bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

local_dir="./data"
hdfs_dir="warehouse"

hdfs dfs -rm -r $hdfs_dir --recursive
hdfs dfs -mkdir -p $hdfs_dir --recursive

for file in "$local_dir"/*; do
    if [ -f "$file" ]; then
        filename=$(basename -- "$file")
        hdfs_path="$hdfs_dir/$filename"
        hdfs dfs -copyFromLocal "$file" "$hdfs_path"
    fi
done
