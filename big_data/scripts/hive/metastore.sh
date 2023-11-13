#!/bin/bash

USERNAME=$(whoami)

hdfs dfs -mkdir /tmp
hdfs dfs -mkdir /user/$USERNAME/warehouse
hdfs dfs -chmod g+w /tmp
hdfs dfs -chmod g+w /user/$USERNAME/warehouse

metastore_path=/tmp/hive-$USERNAME-metastore
rm -rf $metastore_path
mkdir $metastore_path
cd $metastore_path

schematool -dbType derby -initSchema
