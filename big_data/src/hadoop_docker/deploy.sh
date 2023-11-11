#!/usr/bin/env bash

docker compose up -d
docker compose cp hadoop:/home/hduser/hadoop-3.3.3/bin/hdfs $HOME/hadoop-3.3.3
export HADOOP_HOME=$HOME/hadoop-3.3.3
export PATH=$PATH:$HADOOP_HOME/bin
source ~/.bashrc