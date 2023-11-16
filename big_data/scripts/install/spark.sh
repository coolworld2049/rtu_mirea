#!/bin/bash

sudo apt-get install -y default-jre default-jdk scala

SPARK_VERSION=2.4.8
SPARK_HOME=/usr/local/spark

sudo mkdir $SPARK_HOME
sudo chown "$(whoami)":"$(whoami)" -R $SPARK_HOME

sudo wget -nc https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop2.7.tgz -P /tmp
sudo tar -xf /tmp/spark-$SPARK_VERSION-bin-hadoop2.7.tgz -C $SPARK_HOME --strip-components=1

{
  echo "SPARK_HOME=$SPARK_HOME"
  echo "PATH=\$PATH:\$SPARK_HOME/bin"
  echo "export SPARK_HOME"
  echo "export PATH"
} >> ~/.bashrc

echo "Apache Spark $SPARK_VERSION with SparkSQL has been installed to $SPARK_HOME successfully."
echo "Make sure to start a new terminal or run 'source ~/.bashrc' to apply the changes."
