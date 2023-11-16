#!/bin/bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

local_dir="./data"
hdfs_dir="warehouse"

hdfs dfs -mkdir -p $hdfs_dir

for file in "$local_dir"/*; do
    if [ -f "$file" ]; then
        base_filename=$(basename -- "$file")
        filename="${base_filename%.*}"
        hdfs_path=$hdfs_dir/$filename/$base_filename
        hdfs dfs -mkdir -p $hdfs_dir/"$filename"

        hdfs dfs -rm "$hdfs_path"
        echo "Created $hdfs_path"
        hdfs dfs -copyFromLocal "$file" "$hdfs_path"
    fi
done