#!/bin/bash

HIVE_VERSION=3.1.2
HIVE_HOME=/usr/lib/hive

sudo mkdir -p $HIVE_HOME
sudo chown -R $USER:$USER $HIVE_HOME

wget https://downloads.apache.org/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz -P /tmp
tar -xf /tmp/apache-hive-${HIVE_VERSION}-bin.tar.gz -C $HIVE_HOME --strip-components=1

echo "export HIVE_HOME=$HIVE_HOME" >> ~/.bashrc
echo 'export PATH=$PATH:$HIVE_HOME/bin' >> ~/.bashrc
source ~/.bashrc

sudo mkdir -p /etc/hive/conf
sudo cp $HIVE_HOME/conf/*.xml /etc/hive/conf

sudo bash -c "cat > $HIVE_HOME/conf/hive-site.xml <<EOL
<configuration>
<property>
  <name>javax.jdo.option.ConnectionURL</name>
  <value>jdbc:mysql://localhost/metastore?createDatabaseIfNotExist=true</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionDriverName</name>
  <value>com.mysql.jdbc.Driver</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionUserName</name>
  <value>root</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionPassword</name>
  <value>root</value>
</property>

<property>
  <name>datanucleus.autoCreateSchema</name>
  <value>true</value>
</property>

<property>
  <name>datanucleus.fixedDatastore</name>
  <value>true</value>
</property>

<property>
  <name>datanucleus.autoCreateTables</name>
  <value>True</value>
  </property>

</configuration>
EOL"