#!/bin/bash

SPARK_VERSION=2.4.8
SPARK_HOME=/usr/local/spark

sudo mkdir $SPARK_HOME
sudo chown "$(whoami)":"$(whoami)" -R $SPARK_HOME

sudo apt-get install -y openjdk-8-jre openjdk-8-jdk scala
sudo wget -nc https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop2.7.tgz -P /tmp
sudo tar -xf /tmp/spark-$SPARK_VERSION-bin-hadoop2.7.tgz -C $SPARK_HOME --strip-components=1
sudo cp $SPARK_HOME/conf/spark-defaults.conf.template $SPARK_HOME/conf/spark-defaults.conf
sudo cp $SPARK_HOME/conf/spark-env.sh.template  $SPARK_HOME/conf/spark-env.sh
{
  echo "SPARK_HOME=$SPARK_HOME"
  echo "PATH=\$PATH:\$SPARK_HOME/bin"
  echo "HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop"
  echo "LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH"
  echo "export HADOOP_CONF_DIR"
  echo "export LD_LIBRARY_PATH"
  echo "export SPARK_HOME"
  echo "export PATH"
} >> ~/.bashrc

sudo bash -c "cat >> $SPARK_HOME/conf/spark-defaults.conf <<EOL
spark.master yarn
spark.driver.memory 512m
spark.yarn.am.memory 512m
spark.executor.memory 512m
EOL"

sudo bash -c "cat >> $SPARK_HOME/conf/spark-env.conf <<EOL
export PYSPARK_PYTHON=/usr/bin/python3.11
export PYSPARK_DRIVER_PYTHON=/usr/bin/python3.11
EOL"

echo "Apache Spark $SPARK_VERSION with SparkSQL has been installed to $SPARK_HOME successfully."
echo "Make sure to start a new terminal or run 'source ~/.bashrc' to apply the changes."
