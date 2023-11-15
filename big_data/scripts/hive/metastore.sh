#!/bin/bash

hdfs dfs -mkdir /tmp
hdfs dfs -chmod g+w /tmp

hdfs dfs -mkdir /user/"$(whoami)"/warehouse
hdfs dfs -chmod g+w /user/"$(whoami)"/warehouse

METASTORE_PATH="$HOME"/hive-"$(whoami)"-metastore
rm -rf "$METASTORE_PATH"
mkdir "$METASTORE_PATH"
cd "$METASTORE_PATH" || exit

schematool -dbType derby -initSchema
