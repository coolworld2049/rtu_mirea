#!/bin/bash

cd ~

# tar -xvf jdk-8u221-linux-x64.tar.gz

wget http://mirror.linux-ia64.org/apache/hadoop/common/hadoop-2.9.2/hadoop-2.9.2.tar.gz
tar -xvf hadoop-2.9.2.tar.gz

echo "# User specific environment and startup programs" >> ~/.bashrc
echo "JAVA_HOME=$HOME/jdk1.8.0_221" >> ~/.bashrc
echo "HADOOP_HOME=$HOME/hadoop-2.9.2" >> ~/.bashrc
echo "PATH=$PATH:$HOME/.local/bin:$HOME/bin:$JAVA_HOME/bin:$HADOOP_HOME/bin" >> ~/.bashrc
echo "export JAVA_HOME" >> ~/.bashrc
echo "export HADOOP_HOME" >> ~/.bashrc
echo "export PATH" >> ~/.bashrc

mkdir ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

cd ~/hadoop-2.9.2/etc/hadoop

echo "export JAVA_HOME=$HOME/jdk1.8.0_221" >> hadoop-env.sh

cat > core-site.xml <<EOL
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
EOL

cat > hdfs-site.xml <<EOL
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
</configuration>
EOL

cat > mapred-site.xml <<EOL
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>
EOL

cat > yarn-site.xml <<EOL
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

source ~/.bashrc