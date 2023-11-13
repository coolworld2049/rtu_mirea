#!/bin/bash

SCRIPTDIR=$(dirname "$(readlink -f "$0")")

HADOOP_VERSION=2.10.2
HADOOP_HOME=/usr/local/hadoop

cd /tmp
wget -nc http://mirror.linux-ia64.org/apache/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
tar -xzf hadoop-$HADOOP_VERSION.tar.gz
mv hadoop-$HADOOP_VERSION $HADOOP_HOME
cd $SCRIPTDIR

sudo apt install default-jdk
JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
echo "JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
echo "JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
echo "HADOOP_HOME=$HADOOP_HOME" >> ~/.bashrc
echo "PATH=\$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin" >> ~/.bashrc
echo "export JAVA_HOME" >> ~/.bashrc
echo "export HADOOP_HOME" >> ~/.bashrc
echo "export PATH" >> ~/.bashrc
source ~/.bashrc

mkdir ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

cat > $HADOOP_HOME/etc/hadoop/core-site.xml <<EOL
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
EOL

cat > $HADOOP_HOME/etc/hadoop/hdfs-site.xml <<EOL
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
</configuration>
EOL

cat > $HADOOP_HOME/etc/hadoop/mapred-site.xml <<EOL
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>
EOL

cat > $HADOOP_HOME/etc/hadoop/yarn-site.xml <<EOL
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.resourcemanager.address</name>
    <value>127.0.0.1:8032</value>
  </property>
  <property>
    <name>yarn.resourcemanager.scheduler.address</name>
    <value>127.0.0.1:8030</value>
  </property>
  <property>
    <name>yarn.resourcemanager.resource-tracker.address</name>
    <value>127.0.0.1:8031</value>
  </property>
</configuration>
EOL