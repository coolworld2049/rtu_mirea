#!/usr/bin/env bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPTDIR" || exit

. copy_to_hdfs.sh

hdfs dfs -rm -r 'warehouse/output';
pig -f pig/process_data.pig