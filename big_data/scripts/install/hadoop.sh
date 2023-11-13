#!/bin/bash

# Define Hadoop version and installation directory
HADOOP_VERSION=2.10.2
HADOOP_HOME=/usr/local/hadoop

sudo mkdir -p $HADOOP_HOME

if [ -d "$HADOOP_HOME" ]; then
  echo "Apache Hadoop is already installed in $HADOOP_HOME. Exiting."
  exit 0
else
  echo "Downloading and installing Hadoop $HADOOP_VERSION..."
  sudo wget -nc http://mirror.linux-ia64.org/apache/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz -P /tmp
  sudo tar -xzf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C $HADOOP_HOME --strip-components=1
fi

# Install OpenJDK 8
echo "Installing OpenJDK 8..."
sudo apt-get install openjdk-8-jdk
echo "OpenJDK 8 installed successfully."

# Set up Java environment variables
JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
echo "Setting up Java environment variables..."
echo "JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
echo "JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
echo "Java environment variables set up successfully."

# Set up Hadoop environment variables
echo "Setting up Hadoop environment variables..."
echo "HADOOP_HOME=$HADOOP_HOME" >> ~/.bashrc
echo "PATH=\$PATH:\$JAVA_HOME/bin:\$HADOOP_HOME/bin" >> ~/.bashrc
echo "export JAVA_HOME" >> ~/.bashrc
echo "export HADOOP_HOME" >> ~/.bashrc
echo "export PATH" >> ~/.bashrc
echo "Hadoop environment variables set up successfully."

# Set up SSH and generate keys
echo "Setting up SSH and generating keys..."
sudo mkdir -p ~/.ssh
sudo chmod 700 ~/.ssh
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub | sudo tee -a ~/.ssh/authorized_keys
sudo chmod 0600 ~/.ssh/authorized_keys
echo "SSH set up and keys generated successfully."

# Configure Hadoop core-site.xml
echo "Configuring Hadoop core-site.xml..."
sudo bash -c "cat > $HADOOP_HOME/etc/hadoop/core-site.xml <<EOL
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
EOL"
echo "Hadoop core-site.xml configured successfully."

# Configure Hadoop hdfs-site.xml
echo "Configuring Hadoop hdfs-site.xml..."
sudo bash -c "cat > $HADOOP_HOME/etc/hadoop/hdfs-site.xml <<EOL
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
</configuration>
EOL"
echo "Hadoop hdfs-site.xml configured successfully."

# Configure Hadoop mapred-site.xml
echo "Configuring Hadoop mapred-site.xml..."
sudo bash -c "cat > $HADOOP_HOME/etc/hadoop/mapred-site.xml <<EOL
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>
EOL"
echo "Hadoop mapred-site.xml configured successfully."

# Configure Hadoop yarn-site.xml
echo "Configuring Hadoop yarn-site.xml..."
sudo bash -c "cat > $HADOOP_HOME/etc/hadoop/yarn-site.xml <<EOL
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
EOL"
echo "Hadoop yarn-site.xml configured successfully."

echo "Hadoop $HADOOP_VERSION has been installed to $HADOOP_HOME."
