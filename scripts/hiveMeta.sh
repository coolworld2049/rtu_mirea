#!/bin/bash

username="$(whoami)"

hdfs dfs -mkdir /tmp
hdfs dfs -mkdir /user/"$username"/warehouse
hdfs dfs -chmod g+w /tmp
hdfs dfs -chmod g+w /user/"$username"/warehouse

metastore_path=/tmp/hive-$username-metastore
rm -rf "$metastore_path"
mkdir "$metastore_path"
cd "$metastore_path" || exit

schematool -dbType derby -initSchema
