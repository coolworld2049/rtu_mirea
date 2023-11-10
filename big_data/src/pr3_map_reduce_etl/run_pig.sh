#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

hdfs dfs -rm -r 'pr3_map_reduce_etl/output';
pig -f pig/process_data.pig