#!/bin/bash

hdfs dfs -mkdir /user/$USER/warehouse
hdfs dfs -chmod g+w /user/$USER/warehouse

METASTORE_PATH=~/metastore
rm -rf $METASTORE_PATH
mkdir -p $METASTORE_PATH

cd $METASTORE_PATH || exit
schematool -dbType derby -initSchema