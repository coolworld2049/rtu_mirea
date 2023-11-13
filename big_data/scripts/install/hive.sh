#!/bin/bash

# Define Hive version and installation directory
HIVE_VERSION=3.1.2
HIVE_HOME=$HADOOP_OME/hive

if [ -d "$HIVE_HOME" ]; then
  echo "Apache Hive is already installed in $HIVE_HOME."
else
  sudo mkdir -p $HIVE_HOME
  echo "Downloading and installing Hive $HIVE_VERSION..."
  sudo wget -nc https://downloads.apache.org/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz -P /tmp
  sudo tar -xf /tmp/apache-hive-${HIVE_VERSION}-bin.tar.gz -C $HIVE_HOME --strip-components=1
fi

echo "export HIVE_HOME=$HIVE_HOME" >> ~/.bashrc
echo 'export CLASSPATH=$CLASSPATH:$HIVE_HOME/lib/*:' >> ~/.bashrc
echo 'export PATH=$PATH:$HIVE_HOME/bin:' >> ~/.bashrc
source ~/.bashrc

echo "Hive downloaded and installed successfully."

# Copy Hive configuration files to /etc/hive/conf
echo "Copying Hive configuration files..."
sudo mkdir -p /etc/hive/conf
sudo cp $HIVE_HOME/conf/*.xml /etc/hive/conf
echo "Hive configuration files copied successfully."

# Configure Hive metastore in hive-site.xml
echo "Configuring  hive-site.xml..."
sudo bash -c "cat > $HIVE_HOME/conf/hive-site.xml <<EOL
<configuration>

<property>
  <name>hive.metastore.warehouse.dir</name>
  <value>$HOME/warehouse</value>
  <description>location of default database for the warehouse</description>
</property>

<property>
  <name>hadoop.proxyuser.$USER.groups</name>
  <value>*</value>
</property>
<property>
  <name>hadoop.proxyuser.$USER.hosts</name>
  <value>*</value>
</property>

</configuration>
EOL"
echo "Hive metastore configured successfully."

sudo bash -c "cat > /etc/profile.d/hive.sh <<EOL
HADOOP=$HADOOP_HOME/bin/hadoop
export HADOOP
EOL"