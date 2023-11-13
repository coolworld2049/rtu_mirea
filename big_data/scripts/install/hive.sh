#!/bin/bash

HIVE_VERSION=3.1.2
HIVE_HOME=/opt/hive

sudo mkdir -p $HIVE_HOME
sudo chown -R $USER:$USER $HIVE_HOME

wget -nc https://downloads.apache.org/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz -P /tmp
tar -xf /tmp/apache-hive-${HIVE_VERSION}-bin.tar.gz -C $HIVE_HOME --strip-components=1
rm /tmp/apache-hive-${HIVE_VERSION}-bin.tar.gz

echo "export HIVE_HOME=$HIVE_HOME" >> ~/.bashrc
echo 'export PATH=$PATH:$HIVE_HOME/bin' >> ~/.bashrc
source ~/.bashrc

sudo mkdir -p /etc/hive/conf
sudo cp $HIVE_HOME/conf/*.xml /etc/hive/conf