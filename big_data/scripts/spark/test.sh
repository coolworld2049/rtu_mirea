#!/usr/bin/env bash

spark-submit --class org.apache.spark.examples.SparkPi \
--master spark://"$(hostname)":7077 \
--executor-memory 1G \
--total-executor-cores 1 \
"$SPARK_HOME"/examples/jars/spark-examples_2.11-2.4.8.jar 10 2>&1 | grep "Pi is roughly"