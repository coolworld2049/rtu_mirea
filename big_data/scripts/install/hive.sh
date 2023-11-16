#!/bin/bash

# Define Hive version and installation directory
HIVE_VERSION=2.3.9
HIVE_HOME=/usr/local/hive

sudo mkdir "$HIVE_HOME"
sudo chown "$(whoami)":"$(whoami)" -R "$HIVE_HOME"

if [ -d /tmp/apache-hive-${HIVE_VERSION}-bin.tar.gz ]; then
  echo "Apache Hive is already installed in $HIVE_HOME."
else
  echo "Downloading and installing Hive $HIVE_VERSION..."
  sudo wget -nc https://downloads.apache.org/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz -P /tmp
fi

sudo tar -xf /tmp/apache-hive-${HIVE_VERSION}-bin.tar.gz -C "$HIVE_HOME" --strip-components=1

{
  echo "HIVE_HOME=$HIVE_HOME"
  echo "PATH=\$PATH:\$HIVE_HOME/bin"
  echo "export HIVE_HOME"
  echo "export PATH"
} >> ~/.bashrc
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
  <value>/user/$(whoami)/warehouse</value>
  <description>location of default database for the warehouse</description>
</property>

<property>
  <name>hadoop.proxyuser.$(whoami).groups</name>
  <value>*</value>
</property>

<property>
  <name>hadoop.proxyuser.$(whoami).hosts</name>
  <value>*</value>
</property>

<property>
  <name>hive.server2.enable.doAs</name>
  <value>false</value>
</property>

</configuration>
EOL"
echo "Hive hive-site.xml configured successfully."

sudo bash -c "cat > /etc/profile.d/hive.sh <<EOL
HADOOP=$HADOOP_HOME/bin/hadoop
export HADOOP
EOL"

echo "Make sure to start a new terminal or run 'source ~/.bashrc' to apply the changes."
