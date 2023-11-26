#!/bin/bash

"$HADOOP_HOME"/sbin/start-dfs.sh

hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/"$(id -nu)"

"$HADOOP_HOME"/sbin/start-yarn.sh

"$HADOOP_HOME"/sbin/mr-jobhistory-daemon.sh start historyserver
