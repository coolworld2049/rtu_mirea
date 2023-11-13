#!/bin/bash

username="$(whoami)"

hdfs dfs -mkdir /user/$username/warehouse
hdfs dfs -chmod g+w /user/$username/warehouse

metastore_path=/tmp/user/hive-$username-metastore
rm -rf $metastore_path
mkdir -p $metastore_path
cd $metastore_path || exit

schematool -dbType derby -initSchema
schematool -dbType derby -info